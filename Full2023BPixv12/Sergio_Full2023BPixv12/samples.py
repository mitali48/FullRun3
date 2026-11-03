from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False

mcProduction = 'Summer23BPix_130x_nAODv12_Full2023BPixv12'
mcSteps      = 'MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__sblancof__l2tight'
dataReco     = 'Run2023BPix_Prompt_nAODv12_Full2023BPixv12'
dataSteps    = 'DATAl2loose2023BPixv12__sblancof__l2loose'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/'
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
# fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)
fakeDirectory = dataDirectory

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


################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
    ['D','Run2023D-Prompt-v1'],
    ['D','Run2023D-Prompt-v2'],
]

DataSets = ['MuonEG','Muon0','Muon1','EGamma0','EGamma1']

DataTrig = {
    'MuonEG'         : ' Trigger_ElMu' ,
    'Muon0'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'Muon1'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma0'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
    'EGamma1'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
} 

#########################################
############ MC COMMON ##################
#########################################

mcCommonWeightNoMatch = 'XSWeight*METFilter_Common*SFweight'
mcCommonWeight        = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'

###########################################
#############  BACKGROUNDS  ###############
###########################################

########## DY #########
files = nanoGetSampleFiles(mcDirectory, 'DYto2L-2Jets_MLL-50') + nanoGetSampleFiles(mcDirectory, 'DYto2L-2Jets_MLL-10to50')

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 5,
}

########## top #########
files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + nanoGetSampleFiles(mcDirectory, 'TWminusto2L2Nu') + nanoGetSampleFiles(mcDirectory, 'TbarWplusto2L2Nu')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 5
}

########## WW #########
files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name': files,
    'weight': mcCommonWeight + "* wwNLL",
    'FilesPerJob': 5
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
    'weight': mcCommonWeight + " * KFactor_ggWW * (49.63 / 1000)",
    'FilesPerJob': 5
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


########## WZ #########
files = nanoGetSampleFiles(mcDirectory, 'WZ')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight + ' * (gstarHigh)',
    'FilesPerJob': 5
}

########## ZZ #########
files = nanoGetSampleFiles(mcDirectory, 'ZZ')

samples['ZZ'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 5
}

######## Vg ########
files = []
for label in [
        # "ZG",
        "ZG2JtoG2L2J",
        "WGtoLNuG-1J_PTG10to100",
        "WGtoLNuG-1J_PTG100to200",
        "WGtoLNuG-1J_PTG200to400",
        "WGtoLNuG-1J_PTG400to600",
        "WGtoLNuG-1J_PTG600"]:

    files += nanoGetSampleFiles(mcDirectory, label)

samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(Gen_ZGstar_mass <= 0)',
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 5,
}

files = files + nanoGetSampleFiles(mcDirectory, 'WZ')

samples['VgS'] = {
    'name': files,
    'weight': mcCommonWeight,
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 5,
}

#addSampleWeight(samples, 'VgS', "ZG", "(Gen_ZGstar_mass > 0)")
addSampleWeight(samples, 'VgS', "ZG2JtoG2L2J", "(Gen_ZGstar_mass > 0)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG10to100", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1) * (gstarLow * 0.94)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG100to200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1) * (gstarLow * 0.94)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG200to400", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1) * (gstarLow * 0.94)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG400to600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1) * (gstarLow * 0.94)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1) * (gstarLow * 0.94)")
addSampleWeight(samples, 'VgS', "WZ", "(Gen_ZGstar_mass > 0.1) * (gstarLow * 0.94)")

########## VVV #########
files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWW')

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}

###########################################
###############  SIGNALS  #################
###########################################

samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + ' * Weight2MINLO * 1092.7640/1073.2567',
    'FilesPerJob': 3,
}

samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 3,
}


###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
  'name': [],
  'weight': 'METFilter_DATA*fakeW',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 10
}

for _, sd in DataRun:
  for pd in DataSets:
    tag = pd + '_' + sd
    
    files = nanoGetSampleFiles(fakeDirectory, tag)

    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', tag, DataTrig[pd])

    
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
    
