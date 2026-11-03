from mkShapesRDF.lib.search_files import SearchFiles
import os
import inspect
import sys

searchFiles = SearchFiles()
configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))

redirector = ""
useXROOTD = False


mcProduction = 'Summer22EE_130x_nAODv12_Full2022v12' 
mcSteps = 'MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight' 
dataReco = 'Run2022EE_Prompt_nAODv12_Full2022v12'
fakeSteps = 'DATAl2loose2022EEv12__l2loose'
dataSteps = 'DATAl2loose2022EEv12__l2loose'
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
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)
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

# hxs_path = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/lhc-hxswg-YR5'
# sys.path.append(hxs_path)
# from HiggsXSection import HiggsXSection
# HiggsXS = HiggsXSection()


################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
    ['E','Run2022E-Prompt-v1'],
    ['F','Run2022F-Prompt-v1'],
    ['G','Run2022G-Prompt-v1'],
]

DataSets = ['MuonEG','Muon','EGamma']

DataTrig = {
    'MuonEG'         : 'Trigger_ElMu' ,
    'Muon'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)'
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

######### WW #########
files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name': files,
    'weight': mcCommonWeight ,
    # 'weight': mcCommonWeight + "* wwNLL",
    'FilesPerJob': 30
}

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
    'weight': mcCommonWeight + " * 1.6 * (49.63 / 1000)",
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


###########################################
#############  BACKGROUNDS  ###############
###########################################

######### DY #########
files = []
for label in [
        'DYto2Tau-2Jets_MLL-50_0J',
        'DYto2Tau-2Jets_MLL-50_1J',
        'DYto2Tau-2Jets_MLL-50_2J'
        ]:
    files += nanoGetSampleFiles(mcDirectory, label)

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 60
}

########## Top #########
files = []
for label in [
        'TTTo2L2Nu',
        'TbarWplusto2L2Nu',
        'TWminusto2L2Nu',
        ]:
    files += nanoGetSampleFiles(mcDirectory, label)

samples['Top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 40
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
        "DYGto2LG-1Jets_MLL-4to50_PTG-10to100",
        "DYGto2LG-1Jets_MLL-4to50_PTG-100to200",
        "DYGto2LG-1Jets_MLL-4to50_PTG-200",
        "DYGto2LG-1Jets_MLL-50_PTG-10to100",
        "DYGto2LG-1Jets_MLL-50_PTG-100to200",
        "DYGto2LG-1Jets_MLL-50_PTG-200to400",
        "DYGto2LG-1Jets_MLL-50_PTG-400to600",
        "DYGto2LG-1Jets_MLL-50_PTG-600"]:
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

addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-10to100", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-100to200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-10to100", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-100to200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-200to400", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-400to600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J", "(Gen_ZGstar_mass > 0  && Gen_ZGstar_mass <= 4)"),
addSampleWeight(samples, 'VgS', "WZTo3LNu", "(Gen_ZGstar_mass > 4 && Gen_ZGstar_mass < 50)")

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


#####Higgs
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



###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW',
    'weights': [],
    'isData': ['all'],
    'FilesPerJob': 15
}


for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    files = nanoGetSampleFiles(fakeDirectory, datatag)
    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', datatag, DataTrig[pd])

samples['Fake']['subsamples'] = {
  'e': 'abs(Lepton_pdgId[1]) == 11',
  'm': 'abs(Lepton_pdgId[1]) == 13'
}
###########################################
################## DATA ###################
###########################################

samples['DATA'] = { 
    'name': [],  
    'weight': 'LepWPCut*METFilter_DATA',     
    'weights': [], 
    'isData': ['all'], 
    'FilesPerJob': 15 
} 

for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    files = nanoGetSampleFiles(dataDirectory, datatag)
    
    print(datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])
