import sys,os

#: tag used to identify the configuration folder version
tag = "Itr8_muWP_cut_TightID_pfIsoLoose_HWW_tthmva_HWW"
#tag = "2024v15_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoLoose_HWW_tthmva_HWW"   
#tag = "nominal_SR_CR__noJetInHorn_bTag_JES_JER"

#: file to use as runner script, default uses mkShapesRDF.shapeAnalysis.runner, otherwise specify path to script
runnerFile = "default"

#: output file name
outputFile = "mkShapes__{}.root".format(tag)

#: path to ouput folder
outputFolder = "/eos/user/" + os.getlogin()[0] + "/" + os.getlogin() + "/mkShapesRDF_rootfiles/WW2024_Paper/SR_CR/{}/rootFile/".format(tag)
print("Output folder: {}".format(outputFolder))
#outputFolder = "../../../../../../../../../../../../../eos/user/s/sblancof/MC/rootFiles"
#outputFolder = "rootFiles/DY_CR_2024/"

# path to batch folder (used for condor submission)
# batchFolder = "/eos/user/" + os.getlogin()[0] + "/" + os.getlogin() + "/mkShapesRDF_rootfiles/" + tag + "/16Feb2026/condor/"
batchFolder = "condor"

# path to configuration folder (will contain all the compiled configuration files)
configsFolder = "configs"

# luminosity to normalize to (in 1/fb) https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun3Analysis
lumi = 109.0

# file with dict of aliases to define
aliasesFile = "aliases.py"

# file with dict of variables
variablesFile = "variables.py"

# file with dict of cuts
cutsFile = "cuts.py"

# file with dict of samples
samplesFile = "samples.py"

# file with dict of samples
plotFile = "plot.py"

# file with dict of structure (used to define combine processes)
structureFile = "structure.py"

# nuisances file for mkDatacards and for mkShape
nuisancesFile = "nuisances.py"

# path to folder where to save plots
plotPath = "/eos/user/" + os.getlogin()[0] + "/" + os.getlogin() +  "/www/plotsWW2024_paper/SR_CR/{}/".format(tag) 
#plotPath = "Plots"

# this lines are executed right before the runner on the condor node
mountEOS = [
    # "export KRB5CCNAME=/home/gpizzati/krb5\n",
]

# list of imports to import when compiling the whole configuration folder, it should not contain imports used by configuration.py
imports = ["os", "glob", ("collections", "OrderedDict"), "ROOT"]

# list of files to compile
filesToExec = [
    samplesFile,
    aliasesFile,
    variablesFile,
    cutsFile,
    plotFile,
    nuisancesFile,
    structureFile,
]

# list of variables to keep in the compiled configuration folder
varsToKeep = [
    "batchVars",
    "outputFolder",
    "batchFolder",
    "configsFolder",
    "outputFile",
    "runnerFile",
    "tag",
    "samples",
    "aliases",
    "variables",
    ("cuts", {"cuts": "cuts", "preselections": "preselections"}),
    ("plot", {"plot": "plot", "groupPlot": "groupPlot", "legend": "legend"}),
    "nuisances",
    "structure",
    "lumi",
]

# list of variables to keep in the batch submission script (script.py)
batchVars = varsToKeep[varsToKeep.index("samples") :]


varsToKeep += ['plotPath']
