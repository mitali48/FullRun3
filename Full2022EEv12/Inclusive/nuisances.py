mcProduction = 'Summer22EE_130x_nAODv12_Full2022v12' 
mcSteps = 'MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight' 
dataReco = 'Run2022EE_Prompt_nAODv12_Full2022v12'
fakeSteps = 'DATAl2loose2022EEv12__l2loose'
dataSteps = 'DATAl2loose2022EEv12__l2loose'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/'
limitFiles = -1


mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]

redirector = ""

useXROOTD = False

def makeMCDirectory(var=''):
    _treeBaseDir = treeBaseDir + ''
    if useXROOTD:
        _treeBaseDir = redirector + treeBaseDir
    if var== '':
        return '/'.join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return '/'.join([_treeBaseDir, mcProduction, mcSteps + '__' + var])


mcDirectory   = makeMCDirectory()
#######################################################

#merge cuts
cuts0j = []
cuts1j = []
cuts_maj2j = []
total_cuts = []

for k in cuts:
    for cat in cuts[k]['categories']:
        total_cuts.append(k+'_'+cat)
        if '0j' in cat:
            cuts0j.append(k+'_'+cat)
        elif '1j' in cat: 
            cuts1j.append(k+'_'+cat)
        elif 'maj2j' in cat:
            cuts_maj2j.append(k+'_'+cat)
        else: 
            print('WARNING: name of category does not contain either 0j,1j,2j,maj3j,maj2j. Please check cuts.py')



# for k in cuts:
#     for cat in cuts[k]['categories']:
#         if '0j' in cat:
#             cuts0j.append(k+'_'+cat)
#         elif '1j' in cat: 
#             cuts1j.append(k+'_'+cat)
#         elif '2j' in cat and '2j_vbf' not in cat: 
#             cuts2j.append(k+'_'+cat)
#         elif 'maj3j' in cat:
#             cuts_maj3j.append(k+'_'+cat)
#         elif 'maj2j' in cat:
#             cuts_maj2j.append(k+'_'+cat)
#         else: 
#             print('WARNING: name of category does not contain either 0j,1j,2j,maj3j,maj2j. Please check cuts.py')

nuisances = {}

# hxs_path = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/lhc-hxswg-YR5'
# sys.path.append(hxs_path)
# from HiggsXSection import HiggsXSection
# HiggsXS = HiggsXSection()

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity
# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun3
nuisances['lumi_2022EEEE'] = {
    'name'    : 'lumi_2022EEEE',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.014') for skey in mc)
}

nuisances['PU'] = {
    'name': 'pileup_2022EEEE',
    'skipCMS'    : 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['puWeightUp/puWeight', 'puWeightDown/puWeight']) for skey in mc),
    'AsLnN'   : '0'
}     


#### FAKES

nuisances['fake_syst_e'] = {
    'name': 'CMS_fake_syst_e',
    'skipCMS': 1,
    'type': 'lnN',
    'samples': {
        'Fake_e': '1.3'
    },
}

nuisances['fake_syst_m'] = {
    'name': 'CMS_fake_syst_m',
    'skipCMS': 1,
    'type': 'lnN',
    'samples': {
        'Fake_m': '1.3'
    },
}

nuisances['fake_ele'] = {
    'name': 'CMS_fake_e_2022EEEE',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_e': ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name': 'CMS_fake_stat_e_2022EEEE',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_e': ['fakeWStatEleUp', 'fakeWStatEleDown']
    }
}

nuisances['fake_mu'] = {
    'name': 'CMS_fake_m_2022EEEE',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_m': ['fakeWMuUp', 'fakeWMuDown'],
    }
}

nuisances['fake_mu_stat'] = {
    'name': 'CMS_fake_stat_m_2022EEEE',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_m': ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}


##### Trigger Scale Factors                                                                                                                                                                                

trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

nuisances['trigg'] = {
    'name': 'CMS_eff_hwwtrigger_2022EEEE',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, trig_syst) for skey in mc)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'CMS_eff_e_2022EEEE',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc),
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'CMS_eff_m_2022EEEE',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
}


##### Lepton scale
nuisances['lepscale'] = {
    'name': 'CMS_lepscale_2022EEEE',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'leptonScaleup',
    'mapDown': 'leptonScaledo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('leptonScaleup_suffix'),
    'folderDown': makeMCDirectory('leptonScaledo_suffix'),
    'AsLnN': '0'
}
##### Lepton resolution
nuisances['lepres'] = {
    'name': 'CMS_lepres_2022EEEE',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'leptonResolutionup',
    'mapDown': 'leptonResolutiondo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('leptonResolutionup_suffix'),
    'folderDown': makeMCDirectory('leptonResolutiondo_suffix'),
    'AsLnN': '0'
}


nuisances['JER'] = {
    'name': 'CMS_res_j_2022EEEE',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'jerup',
    'mapDown': 'jerdo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('jerup_suffix'),
    'folderDown': makeMCDirectory('jerdo_suffix'),
    'AsLnN': '0'
}

jes_systs    = ["Absolute", "Absolute_2022EE", "FlavorQCD", "BBEC1", "EC2", "HF", "BBEC1_2022EE", "EC2_2022EE", "RelativeBal", "RelativeSample_2022EE", "HF_2022EE"] # Reduced set of 11 uncertainties
#jes_systs = ['jesTotal']

for js in jes_systs:
    
    nuisances[js] = {
        'name'      : 'CMS_scale_j_' + js,
        'skipCMS' : 1,
        'kind'      : 'suffix',
        'type'      : 'shape',
        'mapUp'     : 'jesRegroed_' + js + 'up',
        'mapDown'   : 'jesRegroed_' + js + 'do',
        'samples'   : dict((skey, ['1', '1']) for skey in mc),
        'folderUp'  : makeMCDirectory('jesRegroed_' + js + 'up_suffix'),
        'folderDown': makeMCDirectory('jesRegroed_' + js + 'do_suffix'),
        'AsLnN'     : '0'
    }

nuisances['MET'] = {
    'name': 'CMS_scale_met_2022EE',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'unclustEnup',
    'mapDown': 'unclustEndo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('unclustEnup_suffix'),
    'folderDown': makeMCDirectory('unclustEndo_suffix'),
    'AsLnN': '0'
}

## B-tagger
#Fixed BTV SF variations
for flavour in ['bc', 'light']:
    for corr in ['uncorrelated', 'correlated']:
        btag_syst = [f'btagSF{flavour}_up_{corr}/btagSF{flavour}', f'btagSF{flavour}_down_{corr}/btagSF{flavour}']
        if corr == 'correlated':
            name = f'CMS_btagSF{flavour}_{corr}'
        else:
            name = f'CMS_btagSF{flavour}_2022EE'
        nuisances[f'btagSF{flavour}{corr}'] = {
            'name': name,
            'skipCMS' : 1,
            'kind': 'weight',
            'type': 'shape',
            'samples': dict((skey, btag_syst) for skey in mc),
        }


nuisances['UE_CP5']  = {
    'name'    : 'CMS_ww_UE',
    'skipCMS' : 1,
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc),
}

##rate parameters

rateparams = {
    'DY': {
        'name': 'CMS_ww_DYttnorm',
        'cuts': {
            '0j': cuts0j,
            '1j': cuts1j,
            '2j': cuts_maj2j,
        }
    },
    'Top': {
        'name': 'CMS_ww_Topnorm',
        'cuts': {
            '0j': cuts0j,
            '1j': cuts1j,
            '2j': cuts_maj2j,
        }
    },
    'Fake_e': {
        'name': 'CMS_ww_Fakenorm',
        'cuts': {
            '0j': cuts0j,
            '1j': cuts1j,
            '2j': cuts_maj2j,
        }
    },
    'Fake_m': {
        'name': 'CMS_ww_Fakenorm',
        'cuts': {
            '0j': cuts0j,
            '1j': cuts1j,
            '2j': cuts_maj2j,
        }
    },
}

for process, config in rateparams.items():
    for jetcat, cut in config['cuts'].items():

        nuisances[f'{process}norm{jetcat}'] = {
            'name': f"{config['name']}{jetcat}_2022EE",
            'skipCMS': 1,
            'samples': {process: '1.00'},
            'type': 'rateParam',
            'cuts': cut,
        }

#######xPOG Information : # https://cms-xpog.docs.cern.ch/autoDoc/NanoAODv15/2022EE/doc_TTH-Hto2G_Par-M-125_TuneCP5_13p6TeV_amcatnloFXFX-pythia8_RunIII2022EESummer22NanoAODv15-150X_mcRun3_2022EE_realistic_v2-v2.html

#########PS weights (w_var / w_nominal) [0] isr.murfac=2.0; [1] fsr.murfac=2.0; [2] isr.murfac=0.5; [3] fsr.murfac=0.5
# variations = [ 'PSWeight[0]','PSWeight[1]','PSWeight[2]','PSWeight[3]']
# for skey in mc:
#     nuisances['PS_' + skey + '_ACCEPT'] = {
#         'name'    : 'PS_' + skey + '_ACCEPT',
#         'skipCMS' : 1,
#         'kind'    : 'weight_envelope',
#         'type'    : 'shape',
#         'samples' : { skey: variations},
#         'AsLnN'   : '0',
#     }

nuisances['PS_ISR']  = {
    'name'    : 'PS_ISR',
    'skipCMS' : 1,
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
    'AsLnN'   : '0',
}
nuisances['PS_FSR']  = {
    'name'    : 'PS_FSR',
    'skipCMS' : 1,
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc),
    'AsLnN'   : '0',
}

# ###### pdf uncertainties : Float_t LHE pdf variation weights (w_var / w_nominal) for LHA IDs  320901 - 321000
# pdf_variations = ["LHEPdfWeight[%d]" %i for i in range(1,101)] 


##### Renormalization & factorization scales

variations = ['Alt(LHEScaleWeight,0,1)',
              'Alt(LHEScaleWeight,1,1)',
              'Alt(LHEScaleWeight,3,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

# for skey in mc:
#     if skey not in ['ggWW']:
#         nuisances['QCDscale_' + skey + '_ACCEPT'] = {
#             'name': 'QCDscale_' + skey + '_ACCEPT',
#             'kind': 'weight_envelope',
#             'type': 'shape',
#             'AsLnN': '0',
#             'samples': {skey: variations},
#         }


nuisances['QCDscale_top_ACCEPT']  = {
    'name'  : 'QCDscale_top_ACCEPT',
    'skipCMS' : 1, 
    'kind'  : 'weight_envelope',
    'type'  : 'shape',
    'samples'  : {'Top' : variations}
}

nuisances['QCDscale_DY_ACCEPT'] = {
    'name': 'QCDscale_DY_ACCEPT',
    'skipCMS' : 1,
    'kind'  : 'weight_envelope',
    'type': 'shape',
    'samples': {'DY': variations}
}

nuisances['QCDscale_WW_ACCEPT'] = {
    'name' : 'QCDscale_WW_ACCEPT',
    'skipCMS' : 1,
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'WW'  : variations}
}

nuisances['QCDscale_ggWW_ACCEPT'] = {
    'name': 'QCDscale_ggWW_ACCEPT',
    'skipCMS' : 1,
    'type': 'lnN',
    'samples': {'ggWW': '1.15'},
}

nuisances['QCDscale_WZ_ACCEPT'] = {
    'name' : 'QCDscale_WZ_ACCEPT',
    'skipCMS' : 1,
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'WZ'  : variations}   #ZZ has no variations
}

nuisances['QCDscale_VVV_ACCEPT'] = {
    'name' : 'QCDscale_VVV_ACCEPT',
    'skipCMS' : 1,
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'VVV'  : variations}
}

autoStats = True
if autoStats:
    ## Use the following if you want to apply the automatic combine MC stat nuisances.
    nuisances['stat'] = {
        'type': 'auto',
        'maxPoiss': '10',
        'includeSignal': '0',
        #  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
        #  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)
        'samples': {}
    }