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

# hxs_path = '/eos/user/m/misharma/private/Latinos/HWWRun3/PlotsConfigurationsRun3/WW_Run3/FullRun3/utils/data/lhc-hxswg-YR5'
# sys.path.append(hxs_path)
# from HiggsXSection import HiggsXSection
# HiggsXS = HiggsXSection()


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
    ['Iv1','Run2024I-Prompt-v1'],
    ['Iv2','Run2024I-Prompt-v2'],
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
mcCommonWeight = 'XSWeight'



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

