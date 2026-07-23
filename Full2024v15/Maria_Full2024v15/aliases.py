import os
import copy
import inspect
import ROOT

ROOT.gSystem.Load("libGpad.so")
ROOT.gSystem.Load("libGraf.so")

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3_WH/PlotsConfigurationsRun3/ControlRegions/VgS/2024_v15
configurations = os.path.dirname(configurations) # /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3_WH/PlotsConfigurationsRun3/ControlRegions/VgS/
configurations = os.path.dirname(configurations) # /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3_WH/PlotsConfigurationsRun3/ControlRegions/
configurations = os.path.dirname(configurations) # /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3_WH/PlotsConfigurationsRun3/
print(configurations)

aliases = {}
aliases = OrderedDict()

#mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]
#mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]
mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]


# LepSF3l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67

# LepCut2l__ele_cutBased_MediumID_tthMVA_HWW__mu_cut_TightID_pfIsoLoose_HWW_tthmva_HWW
eleWP = 'cutBased_MediumID_tthMVA_HWW'
muWP  = 'cut_TightID_pfIsoLoose_HWW_tthmva_67'




aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA'],
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc
}

# gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
aliases['PromptGenLepMatch2l'] = {
    'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0)',
    'samples': mc
}

aliases['PromptGenLepMatch1l'] = {
    'expr': '(Alt(Lepton_promptgenmatched, 0, 0) + Alt(Lepton_promptgenmatched, 1, 0) >= 1)',
    'samples': mc
}
###### Top pT reweighting 
aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}

fakerates = '/eos/user/m/mcaserta/Run3_WW/FakeRate/2024_v15_pt'
# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.ProcessLine('fake_rate_reader fr_reader = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"nominal\", 2, \"std\", \"{fakerates}\");')"],
    'expr'           : f'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWEleUp'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleUp = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"EleUp\", 2, \"std\", \"{fakerates}\");')"],
    'expr'           : f'fr_reader_EleUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWEleDown'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleDown = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"EleDown\", 2, \"std\", \"{fakerates}\");')"],
    'expr'           : f'fr_reader_EleDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}   

aliases['fakeWMuUp'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuUp = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"MuUp\", 2, \"std\", \"{fakerates}\");')"],
    'expr'           : f'fr_reader_MuUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'     : ['Fake']
}

aliases['fakeWMuDown'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuDown = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"MuDown\", 2, \"std\", \"{fakerates}\");')"], 
    'expr'           : f'fr_reader_MuDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWStatEleUp'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleUp = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"StatEleUp\", 2, \"std\", \"{fakerates}\");')"],
    'expr'           : f'fr_reader_StatEleUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWStatEleDown'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleDown = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"StatEleDown\", 2, \"std\", \"{fakerates}\");')"],
    'expr'           : f'fr_reader_StatEleDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}
aliases['fakeWStatMuUp'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuUp = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"StatMuUp\", 2, \"std\", \"{fakerates}\");')"],
    'expr'           : f'fr_reader_StatMuUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWStatMuDown'] = {
    'linesToAdd'     : [f'#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuDown = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"StatMuDown\", 2, \"std\", \"{fakerates}\");')"],
    'expr'           : f'fr_reader_StatMuDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}


###### -------------------------------------- 

aliases['gstarLow'] = {
    'expr': 'Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4',
    'samples': ['WZ', 'VgS', 'Vg']
}
aliases['gstarHigh'] = {
    'expr': 'Gen_ZGstar_mass <0 || Gen_ZGstar_mass > 4',
    'samples': ['WZ', 'VgS', 'Vg'],
}


aliases['KFactor_ggWW_NLO'] = {
    'linesToProcess':[
        'ROOT.gSystem.Load("/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/ggww_kfactor_cc.so","", ROOT.kTRUE)',
        "ROOT.gInterpreter.Declare('ggww_K_producer k_reader_GGWW = ggww_K_producer();')"
    ],
    'expr': f'k_reader_GGWW(nLHEPart,LHEPart_pt,LHEPart_eta,LHEPart_phi,LHEPart_mass,LHEPart_pdgId,LHEPart_status)',
    'samples': ['ggWW']
}
aliases['KFactor_ggWW'] = {
    'expr': 'KFactor_ggWW_NLO[0]',
    'samples': ['ggWW']
}
aliases['KFactor_ggWW_Up'] = {
    'expr': 'KFactor_ggWW_NLO[1]',
    'samples': ['ggWW']
}
aliases['KFactor_ggWW_Down'] = {
    'expr': 'KFactor_ggWW_NLO[2]',
    'samples': ['ggWW']
}

aliases['wwNLL'] = {
  'linesToProcess':[
        'ROOT.gSystem.Load("/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/qqww_kfactor_cc.so","", ROOT.kTRUE)',
        """ROOT.gInterpreter.Declare('qqww_K_producer k_reader_QQWW = qqww_K_producer("/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/wwresum/central.dat","/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/wwresum/resum_up.dat", "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/wwresum/resum_down.dat","/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/wwresum/scale_up.dat","/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/wwresum/scale_down.dat");')"""
    ],
    'expr': f'k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,0)',
    'samples': ['WW']
}

aliases['nllW_Rup'] = {
    'expr': f'k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,1,1)',
    'samples': ['WW']
}
aliases['nllW_Rdown'] = {
    'expr': f'k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,-1,1)',
    'samples': ['WW']
}
aliases['nllW_Qup'] = {
    'expr': f'k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,1,0)',
    'samples': ['WW']
}
aliases['nllW_Qdown'] = {
    'expr': f'k_reader_QQWW(GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,GenPart_pdgId,GenPart_status,GenPart_statusFlags,-1,0)',
    'samples': ['WW']
}

aliases['Weight2MINLO'] = {
    'linesToProcess': ['ROOT.gSystem.Load("/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/weight2MINLO_cc.so")'],
    'class': 'Weight2MINLO',
    'args': '"/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/NNLOPS_reweight.root", HTXS_njets30, HTXS_Higgs_pt',
    'samples': ['ggH_hww']
}



# Jet bins
# using Alt(CleanJet_pt, n, 0) instead of Sum(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

# No jet with pt > 30 GeV and eta > 2.5

aliases['zeroJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) < 30.'
}

aliases['oneJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) > 30.'
}

aliases['multiJet'] = {
    'expr': 'Alt(CleanJet_pt, 1, 0) > 30.'
}


aliases['noJetInHorn'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/jet_horns.cc"'],
    'expr': 'Jet_inHorns(CleanJet_pt, CleanJet_eta, true )'
}


aliases['mpmet'] = {
    'expr' : 'min(projtkmet, projpfmet)'
}

########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer23/
########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "DeepFlavB" : {
        "loose"    : "0.0480",
        "medium"   : "0.2435",
        "tight"    : "0.6563",
        "xtight"   : "0.7671",
        "xxtight"  : "0.9483",
    },
    "UParTAK4B" : {
        "loose"    : "0.0246",
        "medium"   : "0.1272",
        "tight"    : "0.4648",
        "xtight"   : "0.6298",
        "xxtight"  : "0.9739",
    },
    "PNetB" : {
        "loose"    : "0.0359",
        "medium"   : "0.1919",
        "tight"    : "0.6133",    
        "xtight"   : "0.7544",
        "xxtight"  : "0.9688",
    }
}

# Algo / SF name
btagging_SFs = {
    "DeepFlavB"      : "deepjet",
    "UParTAK4B"      : "UnifiedParT",
    "PNetB"          : "partNet",
}

# Algorithm and WP selection
bAlgo = 'UParTAK4B' # ['DeepFlavB','RobustParTAK4B','PNetB'] 
bWP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']


# b veto
aliases['bVeto'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 0'.format(bAlgo, btagging_WPs[bAlgo][bWP])
}

# At least one b-tagged jet
aliases['bReq'] = {
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 1'.format(bAlgo, btagging_WPs[bAlgo][bWP])
}


aliases['bReq1'] = {
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && '
            'Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 1'
            .format(bAlgo, btagging_WPs[bAlgo][bWP]),
}

aliases['bReq2'] = {
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && '
            'Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 2'
            .format(bAlgo, btagging_WPs[bAlgo][bWP]),
}


year = '2024_Summer24'
# btv_path =  '/eos/user/m/mcaserta/mkShapes_2026/mkShapesRDF/mkShapesRDF/processor/data/jsonpog-integration/POG/BTV/' + year
shifts = ['central', 'up_uncorrelated', 'down_uncorrelated', 'up_correlated', 'down_correlated']
shift_str = '{"' + '","'.join(shifts) + '"}'

for flavour in ['bc', 'light']:
    btagsf_tmp = 'btagSF_TMP_' + flavour
    aliases[btagsf_tmp] = {
        'linesToProcess':[
            f'ROOT.gSystem.Load("/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/extended/evaluatebtag/evaluate_btagSF{flavour}_cc.so","", ROOT.kTRUE)',
            f"ROOT.gInterpreter.Declare('btagSF{flavour} btag_SF{flavour} = btagSF{flavour}(\"/afs/cern.ch/user/m/mcaserta/private/Run3_WW/mkShapesRDF/FullRun3/data/btag_eff/bTagEff_2024_ttbar_loose.root\",\"{year}\",\"_parT\");')"
        ],
        'expr': f'btag_SF{flavour}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btag{bAlgo}, "L", {shift_str})',
        'samples' : mc,
    }
    for i in range(len(shifts)):
        btagsf = 'btagSF' + flavour
        if shifts[i] != 'central':
            btagsf += '_' + shifts[i]
        aliases[btagsf] = {
            'expr': f"{btagsf_tmp}[{i}]",
            'samples' : mc,
        }


# End of b tagging
##########################################################################

# CR definition

aliases['preSel'] = {
    'expr': 'Lepton_pt[0] > 25. && Lepton_pt[1] > 20. &&(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',
}

aliases['topcr'] = {
    'expr': 'mll > 85 && ( ((zeroJet && !bVeto) || bReq1)  || bReq2 )  && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13', # PuppiMET_pt>20 
}

aliases['dycr'] = {
    'expr': 'mll < 85 && ptll<30 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
}

aliases['sr'] = {
    'expr': 'bVeto && mll>85 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
}
aliases['nHardJets'] = {
    'expr'    :  'Sum(Take(Jet_genJetIdx,CleanJet_jetIdx) >= 0 && Take(GenJet_pt,Take(Jet_genJetIdx,CleanJet_jetIdx)) > 25)',
    'samples' : mc
}



# Data/MC scale factors and systematic uncertainties - Trigger scale factors are missing!
aliases['SFweight'] = {
    # 'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF']),
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', 'btagSFlight']),
    #'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF']),
    #'expr': '1',
    # used to apply leptons SFs
    # 'expr': ' * '.join(['TrigSLWP', 'TrigSLSF', 'RecoSF3l', 'puWeight', 'LepWPCut', 'LepWPSF', 'btagSFbc', 'btagSFlight']),
    'samples': mc
}


aliases['SFweightEleUp'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Up',
    'samples': mc
}
aliases['SFweightEleDown'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Down',
    'samples': mc
}
aliases['SFweightMuUp'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Up',
    'samples': mc
}
aliases['SFweightMuDown'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Down',
    'samples': mc
}

