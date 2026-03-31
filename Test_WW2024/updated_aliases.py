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

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

# LepSF3l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67

# LepSF2l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoLoose_HWW_tthmva_HWW
eleWP = 'cutBased_LooseID_tthMVA_Run3'
muWP  = 'cut_TightID_pfIsoLoose_HWW_tthmva_HWW'

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

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"nominal\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWEleUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleUp = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"EleUp\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader_EleUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWEleDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleDown = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"EleDown\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader_EleDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}   

aliases['fakeWMuUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuUp = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"MuUp\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader_MuUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'     : ['Fake']
}

aliases['fakeWMuDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuDown = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"MuDown\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"], 
    'expr'           : f'fr_reader_MuDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}


aliases['fakeWStatEleUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleUp = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"StatEleUp\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader_StatEleUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWStatEleDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleDown = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"StatEleDown\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader_StatEleDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWStatMuUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuUp = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"StatMuUp\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader_StatMuUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWStatMuDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/utils/macros/fake_rate_reader_class_run3.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuDown = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"StatMuDown\", 2, \"std\", \"{configurations}/utils/data/FakeRate/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader_StatMuDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

###### Top pT reweighting 
aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['Top']
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
        'ROOT.gSystem.Load("/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/ggww_kfactor_cc.so","", ROOT.kTRUE)',
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
        'ROOT.gSystem.Load("/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/qqww_kfactor_cc.so","", ROOT.kTRUE)',
        """ROOT.gInterpreter.Declare('qqww_K_producer k_reader_QQWW = qqww_K_producer("/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/wwresum/central.dat","/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/wwresum/resum_up.dat", "/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/wwresum/resum_down.dat","/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/wwresum/scale_up.dat","/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/wwresum/scale_down.dat");')"""
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
    'linesToProcess': ['ROOT.gSystem.Load("/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/weight2MINLO_cc.so")'],
    'class': 'Weight2MINLO',
    'args': '"/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/NNLOPS_reweight.root", HTXS_njets30, HTXS_Higgs_pt',
    'samples': ['ggH_hww']
}



# Jet bins
# using Alt(CleanJet_pt, n, 0) instead of Sum(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

# No jet with pt > 30 GeV
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
    'expr' : 'Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.5 && abs(CleanJet_eta) < 3.0) == 0',
}


aliases['mpmet'] = {
    'expr' : 'min(projtkmet, projpfmet)'
}

########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer23/
########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "UParTAK4B" : {
        "loose"   : "0.0246",
        "medium"  : "0.1272",
        "tight"   : "0.4648",
        "xtight"  : "0.6298",
        "xxtight" : "0.9739"
    },
}

# Algo / SF name
btagging_SFs = {
    "UParTAK4B" : "upart",
}

# Algorithm and WP selection
bAlgo = 'UParTAK4B'
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

WP_eval = 'L' # ['L', 'M', 'T', 'XT', 'XXT']
tagger = 'UParTAK4'

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]

# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}

# Scale factors
eff_map_year = '2024'
year = '2024' #_Summer24'

shifts_per_flavour = {
    'bc': [
        'central',
        'up' , 'down', 
        'down_bfragmentation','up_bfragmentation',
        'down_correlated','up_correlated',
        'down_fsrdef','up_fsrdef',
        'down_hdamp','up_hdamp',
        'down_isrdef','up_isrdef',
        'down_jer','up_jer',
        'down_jes','up_jes',
        'down_muf','up_muf',
        'down_mur','up_mur',
        'down_pdfas', 'up_pdfas',
        'down_pileup','up_pileup',
        'down_statistic','up_statistic',
        'down_topmass','up_topmass',
        'down_type3','up_type3',
        'down_uncorrelated','up_uncorrelated'
    ],
   'light': [
        'central','down','down_correlated','down_uncorrelated',
        'up','up_correlated','up_uncorrelated'
    ],
}

for flavour in ['bc','light']:

    shifts = shifts_per_flavour[flavour]
    shift_str = '{' + ','.join([f'"{s}"' for s in shifts]) + '}'

    btagsf_tmp = 'btagSF_TMP_' + flavour

    aliases[btagsf_tmp] = {
        'linesToProcess':[
            f'ROOT.gSystem.Load("{configurations}/WW_Run3/FullRun3/extended/evaluate_btagSF{flavour}_cc.so","",ROOT.kTRUE)',
            # f'ROOT.gInterpreter.Declare("btagSF{flavour} btagSF_{flavour}(\"{configurations}/WW_Run3/FullRun3/extended/data/btag_eff/bTagEff_{eff_map_year}_ttbar_loose.root\", \"{year}\", \"_parT\");")'
            f"ROOT.gInterpreter.Declare('btagSF{flavour} btag_SF{flavour} = btagSF{flavour}(\"{configurations}/WW_Run3/FullRun3/data/btag_eff/bTagEff_{eff_map_year}_ttbar_loose.root\",\"2024_Summer24\",\"_parT\");')"
        ],
        # 'expr': f'btagSF_{flavour}(CleanJet_pt,CleanJet_eta,CleanJet_jetIdx,nCleanJet,Jet_hadronFlavour,Jet_btag{bAlgo},"{WP_eval}","{shift}","{tagger}","{year}")',
        'expr': f'btag_SF{flavour}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btag{bAlgo}, "{WP_eval}", {shift_str})',
        'samples': mc,
    }

    for i in range(len(shifts)):

        btagsf = 'btagSF' + flavour
        if shifts[i] != 'central':
            btagsf += '_' + shifts[i]

        aliases[btagsf] = {
            'expr': f"{btagsf_tmp}[{i}]",
            'samples': mc,
        }

# for flavour in ['bc', 'light']:
#     for shift in shifts_per_flavour[flavour]:
#         btagsf = 'btagSF' + flavour
#         if shift != 'central':
#             btagsf += '_' + shift
#         aliases[btagsf] = {
#             'linesToAdd'     : [f'#include "{configurations}/utils/macros/evaluate_btagSF{flavour}.cc"'],
#             'linesToProcess' : [f"ROOT.gInterpreter.Declare('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{configurations}/utils/data/btag/{eff_map_year}/bTagEff_{eff_map_year}_ttbar_{bAlgo}_{WP}.root\", \"{year}\");')"],
#             'expr'           : f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btag{bAlgo}, "{WP_eval}", "{shift}", "{tagger}", "{eff_map_year}")',
#             'samples'        : mc,
#         }

##########################################################################
# End of b tagging
##########################################################################

# CR definition

aliases['topcr'] = {
    'expr': ' mll > 85 && ((zeroJet && !bVeto) || bReq) && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13', # PuppiMET_pt>20 
}

aliases['dycr'] = {
    'expr': 'mll < 85 && ptll<30 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
}

aliases['sr'] = {
    'expr': 'bVeto && mll>85 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
}

# aliases['topcr'] = {
#     'expr': 'mll > 50 && ((zeroJet && !bVeto) || bReq) && mtw2 > 30'
# }
# aliases['dycr'] = {
#     'expr': 'mth < 60 && mll > 40 && mll < 80 && bVeto && mtw2 > 30'
# }
# aliases['wwcr'] = {
#     'expr': 'mth > 60 && mtw2 > 30 && mll > 100 && bVeto'
# }

# SR definition
# aliases['sr'] = {
#     'expr': 'mth > 60 && mtw2 > 30 && bVeto'
# }

# Number of hard (= gen-matched) jets                                                                                                                                                                      
aliases['nHardJets'] = {
    'expr'    :  'Sum(Take(Jet_genJetIdx,CleanJet_jetIdx) >= 0 && Take(GenJet_pt,Take(Jet_genJetIdx,CleanJet_jetIdx)) > 25)',
    'samples' : mc
}

# # Single lepton trigger selection
# aliases['TrigSLWP'] = {
#     'expr' : '(HLT_IsoMu24 || HLT_Ele30_WPTight_Gsf)',
#     'samples' : mc
# }

# aliases['TrigSLSF'] = {
#     'expr' : 'TriggerSFWeight_sngMu * TriggerSFWeight_sngEl',
#     'samples' : mc
# }
    
# # 3-leptons recoSF
# aliases['RecoSF3l'] = {
#     'expr' : 'Lepton_RecoSF[0] * Lepton_RecoSF[1] * Lepton_RecoSF[2]',
#     'samples' : mc
# }


# Data/MC scale factors and systematic uncertainties - Trigger scale factors are missing!
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', 'btagSFlight']), # used to apply leptons SFs
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