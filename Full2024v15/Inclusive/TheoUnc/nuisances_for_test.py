mcProduction = 'Summer24_150x_nAODv15_Full2024v15'
mcSteps      = 'MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight'
dataRecoMuon = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_Muon'
dataRecoEGamma = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_EGamma'
dataRecoMuonEG = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_MuonEG'
dataSteps      = 'DATAl2loose2024v15__l2loose'

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

nuisances = {}

nuisances['PS_ISR_WW']  = {
    'name'    : 'ps_isr',
    'skipCMS' : 1,
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'WW'  : ['PSWeight[2]*NormTHU_WW_ps_isr_Up', 'PSWeight[0]*NormTHU_WW_ps_isr_Down'],
        'ggWW'  : ['PSWeight[2]*NormTHU_ggWW_ps_isr_Up', 'PSWeight[0]*NormTHU_ggWW_ps_isr_Down'],
    },
    'AsLnN'   : '0',
}
nuisances['PS_FSR_WW']  = {
    'name'    : 'ps_fsr',
    'skipCMS' : 1,
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'WW'  : ['PSWeight[3]*NormTHU_WW_ps_fsr_Up', 'PSWeight[1]*NormTHU_WW_ps_fsr_Down'],
        'ggWW'  : ['PSWeight[3]*NormTHU_ggWW_ps_fsr_Up', 'PSWeight[1]*NormTHU_ggWW_ps_fsr_Down'],
    },
    'AsLnN'   : '0',
}

# ###### pdf uncertainties : Float_t LHE pdf variation weights (w_var / w_nominal) for LHA IDs  320901 - 321000
# pdf_variations = ["LHEPdfWeight[%d]" %i for i in range(1,101)] 


##### Renormalization & factorization scales

variations = ['Alt(LHEScaleWeight,0,1)*NormTHU_WW_QCDscale_WW_SPECIAL_NUIS_envelope0',
              'Alt(LHEScaleWeight,1,1)*NormTHU_WW_QCDscale_WW_SPECIAL_NUIS_envelope1',
              'Alt(LHEScaleWeight,3,1)*NormTHU_WW_QCDscale_WW_SPECIAL_NUIS_envelope2',
              'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)*NormTHU_WW_QCDscale_WW_SPECIAL_NUIS_envelope3',
              'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)*NormTHU_WW_QCDscale_WW_SPECIAL_NUIS_envelope4',
              'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)*NormTHU_WW_QCDscale_WW_SPECIAL_NUIS_envelope5']

# for skey in mc:
#     if skey not in ['ggWW']:
#         nuisances['QCDscale_' + skey + '_ACCEPT'] = {
#             'name': 'QCDscale_' + skey + '_ACCEPT',
#             'kind': 'weight_envelope',
#             'type': 'shape',
#             'AsLnN': '0',
#             'samples': {skey: variations},
#         }


nuisances['QCDscale_WW'] = {
    'name' : 'QCDscale_WW',
    'skipCMS' : 1,
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'WW'  : variations}
}
