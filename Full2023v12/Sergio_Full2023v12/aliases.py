
import os
import copy
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]

# LepSF2l__ele_wp90iso__mu_cut_Tight_HWW
eleWP = 'cutBased_LooseID_tthMVA_Run3'
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

# Fake leptons transfer factor --------------------------------------
aliases['fakeW'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"nominal\", 2, \"std\");')"],
    'expr': 'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples'    : ['Fake']
}

# And variations - already divided by central values in formulas !
aliases['fakeWEleUp'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleUp = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"EleUp\", 2, \"std\");')"],
    'expr': 'fr_reader_EleUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples': ['Fake']
}
aliases['fakeWEleDown'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleDown = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"EleDown\", 2, \"std\");')"],
    'expr': 'fr_reader_EleDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples': ['Fake']
}

aliases['fakeWMuUp'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuUp = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"MuUp\", 2, \"std\");')"],
    'expr': 'fr_reader_MuUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples': ['Fake']
}

aliases['fakeWMuDown'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuDown = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"MuDown\", 2, \"std\");')"],
    'expr': 'fr_reader_MuDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples': ['Fake']
}

aliases['fakeWStatEleUp'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleUp = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"StatEleUp\", 2, \"std\");')"],
    'expr': 'fr_reader_StatEleUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples': ['Fake']
}
aliases['fakeWStatEleDown'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleDown = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"StatEleDown\", 2, \"std\");')"],
    'expr': 'fr_reader_StatEleDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples': ['Fake']
}

aliases['fakeWStatMuUp'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuUp = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"StatMuUp\", 2, \"std\");')"],
    'expr': 'fr_reader_StatMuUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples': ['Fake']
}

aliases['fakeWStatMuDown'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuDown = fake_rate_reader(\"2023\", \"Run3\", \"67\", \"StatMuDown\", 2, \"std\");')"],
    'expr': 'fr_reader_StatMuDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_TightID_pfIsoLoose_HWW_tthmva_67, Lepton_isTightElectron_cutBased_LooseID_tthMVA_Run3, CleanJet_pt, nCleanJet)',
    'samples': ['Fake']
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
        'ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/ggww_kfactor_cc.so","", ROOT.kTRUE)',
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
        'ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/qqww_kfactor_cc.so","", ROOT.kTRUE)',
        """ROOT.gInterpreter.Declare('qqww_K_producer k_reader_QQWW = qqww_K_producer("/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/wwresum/central.dat","/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/wwresum/resum_up.dat", "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/wwresum/resum_down.dat","/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/wwresum/scale_up.dat","/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/wwresum/scale_down.dat");')"""
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
    'linesToProcess': ['ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/weight2MINLO_cc.so")'],
    'class': 'Weight2MINLO',
    'args': '"NNLOPS_reweight.root", HTXS_njets30, HTXS_Higgs_pt',
    'samples': ['ggH_hww']
}

# Jet bins
# using Alt(CleanJet_pt, n, 0) instead of Sum(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

# No jet with pt > 30 GeV
aliases['zeroJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) < 30.',
    'afterNuis': True
}

aliases['oneJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) > 30.',
    'afterNuis': True
}

aliases['multiJet'] = {
    'expr': 'Alt(CleanJet_pt, 1, 0) > 30.',
    'afterNuis': True
}

#aliases['noJetInHorn'] = {
#    'expr' : 'Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.6 && abs(CleanJet_eta) < 3.1) == 0',
#}

aliases['noJetInHorn'] = {
    'linesToAdd' : ['#include "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/jet_horns.cc"'],
    'expr': 'Jet_inHorns(CleanJet_pt, CleanJet_eta)',
    'afterNuis': True
}

aliases['noJetInHorn_pT30'] = {
    'expr': 'Jet_inHorns(CleanJet_pt, CleanJet_eta, true)',
    'afterNuis': True
}

aliases['mpmet'] = {
    'expr' : 'min(projtkmet, projpfmet)',
    'afterNuis': True
}

############################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer23BPix/
############################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "DeepFlavB" : {
        "loose"    : "0.0479",
        "medium"   : "0.2435",
    },
    "RobustParTAK4B" : {
        "loose"    : "0.0681",
        "medium"   : "0.3494",
    },
    "PNetB" : {
        "loose"    : "0.0358",
        "medium"   : "0.1919",
    }
}

# Algo / SF name
btagging_SFs = {
    "DeepFlavB"      : "deepjet",
    "RobustParTAK4B" : "RobustParT",
    "PNetB"          : "partNet",
}

# Algorithm and WP selection
bAlgo = 'RobustParTAK4B' # ['DeepFlavB','RobustParTAK4B','PNetB'] 
bWP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']
bSF   = 'deepjet'

# b veto
aliases['bVeto'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 0'.format(bAlgo, btagging_WPs[bAlgo][bWP])
}

# At least one b-tagged jet  
aliases['bReq'] = { 
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 1'.format(bAlgo, btagging_WPs[bAlgo][bWP])
}

year = '2023_Summer23' 
btv_path =  '/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/jsonpog-integration/POG/BTV/' + year
shifts = ['central', 'up_uncorrelated', 'down_uncorrelated', 'up_correlated', 'down_correlated']
shift_str = '{"' + '","'.join(shifts) + '"}'

for flavour in ['bc', 'light']:
    btagsf_tmp = 'btagSF_TMP_' + flavour
    aliases[btagsf_tmp] = {
        'linesToProcess':[
            f'ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/extended/evaluate_btagSF{flavour}_cc.so","", ROOT.kTRUE)',
            f"ROOT.gInterpreter.Declare('btagSF{flavour} btag_SF{flavour} = btagSF{flavour}(\"/afs/cern.ch/work/s/sblancof/private/Run3Analysis/Run2024_ReRecoCDE_PromptFGHI/mkShapesRDF/examples/PlotsConfigurationsRun3/ggH/data/btag_eff/bTagEff_2023_ttbar_loose.root\",\"{year}\",\"_parT\");')"
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


# Top control region
aliases['topcr'] = {
    'expr': 'mth>40 && mpmet>15 && mll > 12 && ((zeroJet && !bVeto) || bReq) && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13', # PuppiMET_pt>20 
    'afterNuis': True
}

aliases['dycr'] = {
    'expr': 'mth<40 && mll>12 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'afterNuis': True
}

aliases['wwcr'] = {
    'expr': 'mth>40 && bVeto && mll>80 && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'afterNuis': True
}

aliases['sr'] = {
    'expr': 'mth>40 && mpmet>15 && bVeto && mll > 12 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'afterNuis': True
}

##########################################################################
# End of b tagging
##########################################################################


# Number of hard (= gen-matched) jets                                                                                                                                                                      
aliases['nHardJets'] = {
    'expr'    :  'Sum(Take(Jet_genJetIdx,CleanJet_jetIdx) >= 0 && Take(GenJet_pt,Take(Jet_genJetIdx,CleanJet_jetIdx)) > 25)',
    'samples' : mc
}

# Data/MC scale factors and systematic uncertainties
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', 'btagSFlight']), # used to apply leptons SFs
    #'expr': ' * '.join(['SFweight2l', 'LepWPCut']), # used just for leptons WP cut
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
