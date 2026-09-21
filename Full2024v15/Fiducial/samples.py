from mkShapesRDF.lib.search_files import SearchFiles
import os
import inspect
import sys

searchFiles = SearchFiles()
configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))

redirector = ""
useXROOTD = False

mcProduction = 'Summer24_150x_nAODv15_Full2024v15'
mcSteps      = 'MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight'
dataRecoMuon = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_Muon'
dataRecoEGamma = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_EGamma'
dataRecoMuonEG = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_MuonEG'
dataSteps      = 'DATAl2loose2024v15__l2loose'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1

def makeMCDirectory(var=""):
    _treeBaseDir = treeBaseDir + ""
    if redirector != "":
        _treeBaseDir = redirector + treeBaseDir
    if var == "":
        return "/".join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return "/".join([_treeBaseDir, mcProduction, mcSteps + "__" + var])


mcDirectory   = makeMCDirectory()
fakeDirectoryMuon = os.path.join(treeBaseDir, dataRecoMuon, dataSteps)
dataDirectoryMuon = os.path.join(treeBaseDir, dataRecoMuon, dataSteps)
fakeDirectoryEGamma = os.path.join(treeBaseDir, dataRecoEGamma, dataSteps)
dataDirectoryEGamma = os.path.join(treeBaseDir, dataRecoEGamma, dataSteps)
fakeDirectoryMuonEG = os.path.join(treeBaseDir, dataRecoMuonEG, dataSteps)
dataDirectoryMuonEG = os.path.join(treeBaseDir, dataRecoMuonEG, dataSteps)

samples = {}


def nanoGetSampleFiles(path, name):
    _files = searchFiles.searchFiles(path, name, redirector=redirector)
    if limitFiles != -1 and len(_files) > limitFiles:
        return [(name, _files[:limitFiles])]
    else:
        return [(name, _files)]


def CombineBaseW(samples, proc, samplelist):
    _filtFiles = list(filter(lambda k: k[0] in samplelist, samples[proc]["name"]))
    _files = list(map(lambda k: k[1], _filtFiles))
    _l = list(map(lambda k: len(k), _files))
    leastFiles = _files[_l.index(min(_l))]
    dfSmall = ROOT.RDataFrame("Runs", leastFiles)
    s = dfSmall.Sum("genEventSumw").GetValue()
    f = ROOT.TFile(leastFiles[0])
    t = f.Get("Events")
    t.GetEntry(1)
    xs = t.baseW * s

    __files = []
    for f in _files:
        __files += f
    df = ROOT.RDataFrame("Runs", __files)
    s = df.Sum("genEventSumw").GetValue()
    newbaseW = str(xs / s)
    weight = newbaseW + "/baseW"

    for iSample in samplelist:
        addSampleWeight(samples, proc, iSample, weight)


def addSampleWeight(samples, sampleName, sampleNameType, weight):
    obj = list(filter(lambda k: k[0] == sampleNameType, samples[sampleName]["name"]))[0]
    samples[sampleName]["name"] = list(
        filter(lambda k: k[0] != sampleNameType, samples[sampleName]["name"])
    )
    if len(obj) > 2:
        samples[sampleName]["name"].append(
            (obj[0], obj[1], obj[2] + "*(" + weight + ")")
        )
    else:
        samples[sampleName]["name"].append((obj[0], obj[1], "(" + weight + ")"))

hxs_path  = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/utils/data/lhc-hxswg-YR5'
sys.path.append(hxs_path)

from HiggsXSection import HiggsXSection
HiggsXS = HiggsXSection()

################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
    ['C','Run2024C-ReReco-v1'],
    ['D','Run2024D-ReReco-v1'],
    ['E','Run2024E-ReReco-v1'],
    ['F','Run2024F-Prompt-v1'],
    ['G','Run2024G-Prompt-v1'],
    ['H','Run2024H-Prompt-v1'],
    ['I','Run2024I-Prompt-v1'],
]

DataSets = ['MuonEG','Muon0','Muon1','EGamma0','EGamma1']

DataTrig = {
    'MuonEG'          :  'Trigger_ElMu' ,
    #'SingleMuon'     : '!Trigger_ElMu && Trigger_sngMu' ,
    'Muon0'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'Muon1'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma0'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
    'EGamma1'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
}


#########################################
############ MC COMMON ##################
#########################################

# SFweight include btag weights
mcCommonWeightNoMatch = 'XSWeight*METFilter_Common*SFweight'
mcCommonWeight1Match  = 'XSWeight*METFilter_Common*PromptGenLepMatch1l*SFweight'
mcCommonWeight        = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'

#mcCommonWeight = 'XSWeight*METFilter_Common*SFweight'


###########################################
###############  SIGNALS  #################
########################################### 
signals =[]
######### WW #########
files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name': files,
    'weight': mcCommonWeight ,
    # 'weight': mcCommonWeight + "* wwNLL",
    'FilesPerJob': 30
}
signals.append('WW')

########## ggWW #########
files = []
for label in [
        "GluGlutoContintoWWtoENuENu",
        "GluGlutoContintoWWtoENuMuNu",
	    "GluGlutoContintoWWtoENuTauNu",
        "GluGlutoContintoWWtoMuNuENu",
        "GluGlutoContintoWWtoMuNuMuNu",
        "GluGlutoContintoWWtoMuNuTauNu",
        "GluGlutoContintoWWtoTauNuENu",
        "GluGlutoContintoWWtoTauNuMuNu",
        "GluGlutoContintoWWtoTauNuTauNu"]:

    files += nanoGetSampleFiles(mcDirectory, label)

samples['ggWW'] = {
    'name': files,
    'weight': mcCommonWeight + " * KFactor_ggWW * (49.63 / 1000)",
    'FilesPerJob': 50
}

addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoENuENu", "1.0 / 0.0744")
addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoENuMuNu", "1.0 / 0.0749")
addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoENuTauNu", "1.0 / 0.0790")
addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoMuNuENu", "1.0 / 0.0749")
addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoMuNuMuNu", "1.0 / 0.0753")
addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoMuNuTauNu", "1.0 / 0.0795")
addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoTauNuENu", "1.0 / 0.0790")
addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoTauNuMuNu", "1.0 / 0.0795")
addSampleWeight(samples, 'ggWW', "GluGlutoContintoWWtoTauNuTauNu", "1.0 / 0.0840")

signals.append('ggWW')

nbins = 4

for sname in signals:
  sample = samples[sname]
  sample['subsamples'] = {}

  sample['subsamples']['nonfid'] = '!(fid)'

  for i in range(nbins):
    #   sample['subsamples']['B%d'%i] = 'fid && B%d'%i
    sample['subsamples'][f'B{i}'] =  f'fid && B{i}'


###########################################
#############  BACKGROUNDS  ###############
###########################################

######### DY #########
files = []
for label in [
        'DYto2E-2Jets_MLL-50',
        'DYto2Mu-2Jets_MLL-50',
        'DYto2Tau-2Jets_MLL-50',
        'DYto2E-2Jets_MLL-10to50',
        'DYto2Mu-2Jets_MLL-10to50',
        'DYto2Tau-2Jets_MLL-10to50'
        ]:
    files += nanoGetSampleFiles(mcDirectory, label)

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 40
}

########## Top #########
files = []
for label in [
        'TTTo2L2Nu',
        'TbarWplusto2L2Nu',
        'TWminusto2L2Nu',
        'ST_t-channel_top',
        'ST_t-channel_antitop',
        'ST_s-channel_plus',
        'ST_s-channel_minus'
        ]:
    files += nanoGetSampleFiles(mcDirectory, label)

samples['Top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 20
}
addSampleWeight(samples,'Top','TTTo2L2Nu','Top_pTrw')

########## WZ #########
files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight +  ' * (Gen_ZGstar_mass >= 50)',
    'FilesPerJob': 50
}

########## ZZ #########
files = nanoGetSampleFiles(mcDirectory, 'ZZ')

samples['ZZ'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 50
}

# Vg/Vgstar

######## Vg ########
files = []
for label in [
        "WGtoLNuG-1J",
        "DYGto2LG-1Jets_Bin-MLL-4to50",
        "DYGto2LG-1Jets_Bin-MLL-50"]:
#
    files += nanoGetSampleFiles(mcDirectory, label)
#
samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(Gen_ZGstar_mass <= 0)',
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob':60,
}
##########VgS#########
files = files + nanoGetSampleFiles(mcDirectory, 'WZTo3LNu')

samples['VgS'] = {
    'name': files,
    'weight': mcCommonWeight,
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 60,
}

addSampleWeight(samples, 'VgS', "WGtoLNuG-1J", "(Gen_ZGstar_mass > 0  && Gen_ZGstar_mass < 4)"),
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_Bin-MLL-50", "(Gen_ZGstar_mass > 0)"),
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_Bin-MLL-4to50", "(Gen_ZGstar_mass > 0)"),
addSampleWeight(samples, 'VgS', "WZTo3LNu", "(Gen_ZGstar_mass >= 4 && Gen_ZGstar_mass < 50)")


# #Zg        
# files = nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_Bin-MLL-50') + \
#         nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_Bin-MLL-4to50')

# samples['Zg'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*(Gen_ZGstar_mass <= 0)',
#     'FilesPerJob': 30,
# }

# #Wg
# files = nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J')

# samples['Wg'] = {
#     'name': files,
#     'weight': mcCommonWeight1Match + '*(Gen_ZGstar_mass <= 0)',
#     'FilesPerJob': 30,
# }

# #ZgS
# files = nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_Bin-MLL-4to50') + \
#         nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_Bin-MLL-50')
        

# samples['ZgS'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*(Gen_ZGstar_mass > 0)', #the photon is virtual we can reconstruct its mass
#     'FilesPerJob': 80,
# }



# # addSampleWeight(samples, 'ZgS', "DYGto2LG-1Jets_Bin-MLL-4to50", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
# # addSampleWeight(samples, 'ZgS', "DYGto2LG-1Jets_Bin-MLL-50", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")

# # WgS
# files = nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J') + \
#         nanoGetSampleFiles(mcDirectory, "WZTo3LNu")

# samples['WgS'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 80,
# }

# addSampleWeight(samples, 'WgS', "WGtoLNuG-1J", "(Gen_ZGstar_mass > 0  && Gen_ZGstar_mass < 4)")
# addSampleWeight(samples, 'WgS', "WZTo3LNu",    "(Gen_ZGstar_mass >= 4 && Gen_ZGstar_mass < 50)")


########## Multibosons VVV #########
files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWW')

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 50
}

###########################################
###############  HWW  #################
########################################### 


# files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'HZJ_HToWW_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'GluGluZH_HToWWTo2L2Nu_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWW_M125') + nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWW_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'ZHToTauTau_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'WplusHToTauTau_M125') + nanoGetSampleFiles(mcDirectory, 'WminusHToTauTau_M125')

# files = []
# for label in [
#         "GluGluHToWWTo2L2Nu_M125",
#         "VBFHToWWTo2L2Nu_M125",
#         "GluGluHToTauTau_M125_Powheg",
#         "VBFHToTauTau_M125",
#         "ttHToNonbb_M125",
#         "HWplusJ_HToWWTo2L2Nu_WToLNu_M125",
#         "HWplusJ_HToWWTo2L2Nu_WTo2Q_M125",
#         "HWminusJ_HToWWTo2L2Nu_WToLNu_M125",
#         "HWminusJ_HToWWTo2L2Nu_WTo2Q_M125",
#         "ZH_Zto2L_Hto2Wto2L2Nu_M125",
#         "ZH_Zto2Q_Hto2Wto2L2Nu_M125",
#         "GluGluZH_Zto2L_Hto2Wto2L2Nu_M125",
#         "GluGluZH_Zto2Q_Hto2Wto2L2Nu_M125",]:

#     files += nanoGetSampleFiles(mcDirectory, label)

# samples['Higgs'] = {
#     'name' : files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 8
# }

# addSampleWeight(samples, 'Higgs', "GluGluHToWWTo2L2Nu_M125", "{HiggsXS.GetHiggsProdXS('ggH', '125.38')} / 51.960"),
# addSampleWeight(samples, 'Higgs', "VBFHToWWTo2L2Nu_M125", "{HiggsXS.GetHiggsProdXS('vbfH', '125.38')} / 4.067"),
# addSampleWeight(samples, 'Higgs', "GluGluHToTauTau_M125_Powheg", "{HiggsXS.GetHiggsProdXS('ggH', '125.38')} / 51.960"),
# addSampleWeight(samples, 'Higgs', "VBFHToTauTau_M125", "{HiggsXS.GetHiggsProdXS('vbfH', '125.38')} / 4.067"),
# addSampleWeight(samples, 'Higgs', "ttHToNonbb_M125", "{HiggsXS.GetHiggsProdXS('ttH', '125.38')} / 0.564"),
# addSampleWeight(samples, 'Higgs', "HWplusJ_HToWWTo2L2Nu_WToLNu_M125", "{HiggsXS.GetHiggsProdXS('HWplus', '125.38')} / 0.8801"),
# addSampleWeight(samples, 'Higgs', "HWplusJ_HToWWTo2L2Nu_WTo2Q_M125", "{HiggsXS.GetHiggsProdXS('HWplus', '125.38')} / 0.8801"),
# addSampleWeight(samples, 'Higgs', "HWminusJ_HToWWTo2L2Nu_WToLNu_M125", "{HiggsXS.GetHiggsProdXS('HWminus', '125.38')} / 0.5620"),
# addSampleWeight(samples, 'Higgs', "HWminusJ_HToWWTo2L2Nu_WTo2Q_M125", "{HiggsXS.GetHiggsProdXS('HWminus', '125.38')} / 0.5620"),
# addSampleWeight(samples, 'Higgs', "ZH_Zto2L_Hto2Wto2L2Nu_M125", "{HiggsXS.GetHiggsProdXS('ZH', '125.38')} / 0.8014"),
# addSampleWeight(samples, 'Higgs', "ZH_Zto2Q_Hto2Wto2L2Nu_M125", "{HiggsXS.GetHiggsProdXS('ZH', '125.38')} / 0.8014"),
# addSampleWeight(samples, 'Higgs', "GluGluZH_Zto2L_Hto2Wto2L2Nu_M125", "{HiggsXS.GetHiggsProdXS('ggZH', '125.38')} / 0.1347"),
# addSampleWeight(samples, 'Higgs', "GluGluZH_Zto2Q_Hto2Wto2L2Nu_M125", "{HiggsXS.GetHiggsProdXS('ggZH', '125.38')} / 0.1347")


# ### ggH -> WW
# files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')

# samples['ggH_hww'] = {
#     'name': files,
#     'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('ggH', '125.38')} / 51.960",
#     'FilesPerJob': 10,
# }

# ### VBF H->WW
# files = nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125')

# samples['qqH_hww'] = {
#     'name': files,
#     'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('vbfH', '125.38')} / 4.067",
#     'FilesPerJob': 10,
# }

# ### ZH H->WW
# files = nanoGetSampleFiles(mcDirectory, 'ZH_Zto2L_Hto2Wto2L2Nu_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'ZH_Zto2Q_Hto2Wto2L2Nu_M125') 

# samples['ZH_hww'] = {
#     'name':   files,
#     'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('ZH', '125.38')} / 0.8014",
#     'FilesPerJob': 10,
# }

# files = nanoGetSampleFiles(mcDirectory, 'GluGluZH_Zto2L_Hto2Wto2L2Nu_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'GluGluZH_Zto2Q_Hto2Wto2L2Nu_M125') 

# samples['ggZH_hww'] = {
#     'name':   files,
#     'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('ggZH', '125.38')} / 0.1347",
#     'FilesPerJob': 10,
# }

# ### WH H->WW
# files = nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWWTo2L2Nu_WToLNu_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWWTo2L2Nu_WTo2Q_M125')  + \
#         nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWWTo2L2Nu_WToLNu_M125') + \
#         nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWWTo2L2Nu_WTo2Q_M125') 

# samples['WH_hww'] = {
#     'name':   files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 10,
# }

# addSampleWeight(samples, 'WH_hww', "HWplusJ_HToWWTo2L2Nu_WToLNu_M125", f"{HiggsXS.GetHiggsProdXS('HWplus', '125.38')} / 0.8801")
# addSampleWeight(samples, 'WH_hww', "HWplusJ_HToWWTo2L2Nu_WTo2Q_M125", f"{HiggsXS.GetHiggsProdXS('HWplus', '125.38')} / 0.8801")
# addSampleWeight(samples, 'WH_hww', "HWminusJ_HToWWTo2L2Nu_WToLNu_M125", f"{HiggsXS.GetHiggsProdXS('HWminus', '125.38')} / 0.5620")
# addSampleWeight(samples, 'WH_hww', "HWminusJ_HToWWTo2L2Nu_WTo2Q_M125", f"{HiggsXS.GetHiggsProdXS('HWminus', '125.38')} / 0.5620")

# ### ttH -> WW
# files = nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125')

# samples['ttH_hww'] = {
#     'name':   files,
#     'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('ttH', '125.38')} / 0.564",
#     'FilesPerJob': 10,
# }

# ### H->TauTau
# files = nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125_Powheg')

# samples['ggH_htt'] = {
#     'name':   files,
#     'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('ggH', '125.38')} / 51.960",
#     'FilesPerJob': 10,
# }

# files = nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125')

# samples['qqH_htt'] = {
#     'name':   files,
#     'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('vbfH', '125.38')} / 4.067",
#     'FilesPerJob': 10,
# }


samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight ,
    # 'weight': mcCommonWeight + ' * Weight2MINLO * 1092.7640/1073.2567',
    'FilesPerJob': 50
}

samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 50
}

###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW',
    'weights': [],
    'isData': ['all'],
    'FilesPerJob': 100
}


for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    if datatag.startswith('MuonEG'):
        files = nanoGetSampleFiles(fakeDirectoryMuonEG, datatag)
    elif datatag.startswith('Muon'):
        files = nanoGetSampleFiles(fakeDirectoryMuon, datatag)
    elif datatag.startswith('EGamma'):
        files = nanoGetSampleFiles(fakeDirectoryEGamma, datatag)

    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', datatag, DataTrig[pd])

###########################################
################## DATA ###################
###########################################

samples['DATA'] = { 
    'name': [],  
    'weight': 'LepWPCut*METFilter_DATA',     
    'weights': [], 
    'isData': ['all'], 
    'FilesPerJob': 100
} 

for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    if datatag.startswith('MuonEG'):
        files = nanoGetSampleFiles(dataDirectoryMuonEG, datatag)
    elif datatag.startswith('Muon'):
        files = nanoGetSampleFiles(dataDirectoryMuon, datatag)
    elif datatag.startswith('EGamma'):
        files = nanoGetSampleFiles(dataDirectoryEGamma, datatag)
    
    print(datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])

