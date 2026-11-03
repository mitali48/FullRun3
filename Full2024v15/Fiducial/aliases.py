import os
import copy
import inspect
import ROOT
import json

ROOT.gSystem.Load("libGpad.so")
ROOT.gSystem.Load("libGraf.so")
ROOT.gSystem.Load("libc.so")

macros = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/macros/'
fakerates = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/FakeRate/'
btagmaps = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/btag/'
extended='/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/extended/'
print(macros)
print(fakerates)
print(btagmaps)
print(extended)

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]

# LepSF2l__ele_cutBased_MediumID_tthMVA_Run3__mu_cut_TightID_pfIsoLoose_HWW_tthmva_67
eleWP = 'cutBased_MediumID_tthMVA_Run3'
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
    'samples': ['Top']
}

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd'     : [f'#include "{macros}fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.ProcessLine('fake_rate_reader fr_reader = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"nominal\", 2, \"std\", \"{fakerates}\", \"2024_v15_pt\");')"],
    'expr'           : f'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

for stat in ['','Stat']:
    for lep in ['Ele','Mu']:
        for variation in ['Up','Down']:
            aliases['fakeW'+stat+lep+variation] = {
                'linesToAdd'     : [f'#include "{macros}fake_rate_reader_class.cc"'],
                'linesToProcess' : [f"ROOT.gInterpreter.ProcessLine('fake_rate_reader fr_reader{stat}{lep}{variation} = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"{stat}{lep}{variation}\", 2, \"std\", \"{fakerates}\", \"2024_v15_pt\");')"],
                'expr'           : f'fr_reader{stat}{lep}{variation}(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
                'samples'        : ['Fake']
            }


########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer23/
########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "UParTAK4B": {
        "loose": 0.0246,
        "medium": 0.1272,
        "tight": 0.4648,
        "xtight": 0.6298,
        "xxtight": 0.9739,
    },
}
# Algo / SF name
btagging_SFs = {
    "UParTAK4B"      : "upart",
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
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}

aliases['bReq1'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 1'
}

aliases['bReq2'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 2'
}
eff_map_year = '2024' # ['2022', '2022EE', '2023', '2023BPix']
year = 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15' # ['Run3-22CDSep23-Summer22-NanoAODv12', 'Run3-22EFGSep23-Summer22EE-NanoAODv12, 'Run3-23CSep23-Summer23-NanoAODv12', 'Run3-23DSep23-Summer23BPix-NanoAODv12', 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15']

for flavour in ['bc', 'light']:
    for shift in ['central', 'down_correlated', 'down_uncorrelated', 'up_correlated', 'up_uncorrelated']:
        btagsf = 'btagSF' + flavour
        if shift != 'central':
            btagsf += '_' + shift
        aliases[btagsf] = {
            'linesToAdd': [f'#include "{macros}evaluate_btagSF{flavour}.cc"'],
            'linesToProcess': [f"ROOT.gInterpreter.ProcessLine('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{btagmaps}/{eff_map_year}/bTagEff_{eff_map_year}_ttbar_{bAlgo}_loose.root\", \"{year}\");')"],
            'expr': f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btag{bAlgo}, "{WP_eval}", "{shift}", "{tagger}","{eff_map_year}")',
            'samples' : mc,
        }

##########################################################################
# End of b tagging
##########################################################################


# Jet bins
# using Alt(CleanJet_pt, n, 0) instead of Sum(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples
# No jet with pt > 30 GeV and eta > 2.5

aliases['zeroJet'] = {
    'expr': 'Alt(CleanJet_pt,0, 0.0)<30.0'
}

aliases['oneJet'] = {
    'expr': 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 '
}

aliases['twoJet'] = {
    'expr': 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)>30.0 && Alt(CleanJet_pt,2, 0.0)<30.0'
}

aliases['multiJet'] = {
    'expr': 'Sum(CleanJet_pt>30.0)>=3'
}

aliases['noJetInHorn'] = {
    'linesToAdd' : [f'#include "{extended}jet_horns.cc"'],
    'expr': 'Jet_inHorns(CleanJet_pt, CleanJet_eta, true )'
}



##########################################################################
## Number of clean generator-level jets
##########################################################################
# aliases['nCleanGenJets'] = {
#     'linesToAdd'     : [f'#include "{extended}/CleanGenJet.cc"'],
#     'linesToProcess' : ['ROOT.gInterpreter.Declare(\'CleanGenJet cleaner("njet");\')'],
#     'expr': 'cleaner(GenJet_pt, GenJet_eta, GenJet_phi, GenPart_pt, GenPart_eta, GenPart_phi, LeptonGen_isPrompt)',
#     'samples': ['WW', 'ggWW']
# }

# aliases['B0'] = {
#     'expr': 'nCleanGenJets == 0',
#     'samples': ['WW', 'ggWW']
# }

# aliases['B1'] = {
#     'expr': 'nCleanGenJets == 1',
#     'samples': ['WW', 'ggWW']
# }

# aliases['B2'] = {
#     'expr': 'nCleanGenJets >= 2',
#     'samples': ['WW', 'ggWW']
# }   

# aliases['B3'] = {
#     'expr': 'nCleanGenJets >= 3',
#     'samples': ['WW', 'ggWW']
# }

aliases['fid'] = {
    'linesToAdd'     : [f'#include "{extended}/fiducial_script.cc"'],
    # 'expr': 'FiducialGen(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_status, GenPart_genPartIdxMother)',
    'expr': 'FiducialGen(GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_mass, GenDressedLepton_pdgId, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_status, GenPart_genPartIdxMother)',
    'samples': ['WW', 'ggWW']
}

aliases['nGenJetFiducial'] = {
    'linesToAdd': [ f'#include "{extended}/fiducial_script.cc"'],
    # 'expr': 'GetNGenJets(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_status, GenPart_genPartIdxMother)',
    # 'expr': 'GetNGenJets(GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_mass, DressedLepton_pdgId, GenDressedLepton_hasTauAnc, GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_status, GenPart_genPartIdxMother, GenJet_pt, GenJet_eta, GenJet_phi)',
    'expr': 'GetNGenJets(GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenJet_pt, GenJet_eta, GenJet_phi)',
    'samples': ['WW', 'ggWW']
}

aliases['B0'] = {
    'expr': 'nGenJetFiducial == 0',
    'samples': ['WW', 'ggWW']
}

aliases['B1'] = {
    'expr': 'nGenJetFiducial == 1',
    'samples': ['WW', 'ggWW']
}

aliases['B2'] = {
    'expr': 'nGenJetFiducial >= 2',
    'samples': ['WW', 'ggWW']
}   

aliases['B3'] = {
    'expr': 'nGenJetFiducial >= 3',
    'samples': ['WW', 'ggWW']
}

# aliases['DressedLeptonGen_pdgId'] = {

#     'linesToAdd': [
#         f'#include "{extended}/fiducial_Gen.cc"'
#     ],

#     'expr': 'GetDressedLeptonGen_pdgId(GenPart_pt, GenPart_eta, '
#             'GenPart_phi, GenPart_mass, GenPart_pdgId, '
#             'GenPart_status, GenPart_genPartIdxMother)',

#     'samples': ['WW', 'ggWW']

# }

# aliases['DressedLeptonGen_pt'] = {

#     'linesToAdd': [
#         f'#include "{extended}/fiducial_Gen.cc"'
#     ],

#     'expr': 'GetDressedLeptonGen_pt(GenPart_pt, GenPart_eta, '
#             'GenPart_phi, GenPart_mass, GenPart_pdgId, '
#             'GenPart_status, GenPart_genPartIdxMother)',

#     'samples': ['WW', 'ggWW']

# }

# aliases['DressedLeptonGen_OriginalMotherPID'] = {

#     'linesToAdd': [
#         f'#include "{extended}/fiducial_Gen.cc"'
#     ],

#     'expr': 'GetDressedLeptonGen_OriginalMotherPID('
#             'GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, '
#             'GenPart_pdgId, GenPart_status, GenPart_genPartIdxMother)',

#     'samples': ['WW', 'ggWW']

# }

# aliases['DressedLeptonGen_FromTau'] = {
#     'linesToAdd': [ f'#include "{extended}/fiducial_Gen.cc"'],

#     'expr': 'GetDressedLeptonGen_FromTau('
#             'GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, '
#             'GenPart_pdgId, GenPart_status, GenPart_genPartIdxMother)',

#     'samples': ['WW', 'ggWW']

# }



# custom variables 
aliases['mpmet'] = {
    'expr' : 'min(projtkmet, projpfmet)'
}

# Data/MC scale factors and systematic uncertainties
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', ' btagSFlight']),
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