#!/usr/bin/env python                                                                                                                                                                                                                                                           

import sys
import optparse
import copy
import collections
import os.path
import math
import logging
import tempfile
import subprocess
import fileinput
import argparse
from sys import argv
import ROOT

######
######
######

filename = "/eos/user/s/sblancof/MC/rootFiles/mkShapes__HWW_2022.root"

######
######
######

from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib
configsFolder = "configs"
ConfigLib.loadLatestPickle(os.path.abspath(configsFolder), globals())
print(dir())
print(globals().keys())


cuts = cuts["cuts"]
inputFile = outputFolder + "/" + outputFile

ROOT.TH1.SetDefaultSumw2(True)

import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils

subsamplesmap = utils.flatten_samples(samples)
categoriesmap = utils.flatten_cuts(cuts)

from mkShapesRDF.shapeAnalysis.histo_utils import postProcessNuisances

nuisances_to_process = {}
for nuisance in nuisances.keys():
    if not (
            nuisances[nuisance].get("kind", "").endswith("envelope")
            or nuisances[nuisance].get("kind", "").endswith("rms")
            or nuisances[nuisance].get("kind", "").endswith("square")
    ):
        continue

    nuisances_to_process[nuisance] = nuisances[nuisance]

print("Nuisances to postprocess:")
print(nuisances_to_process.keys())
print("\n")

for nuisance in nuisances_to_process:
    print(nuisance)
    tmp_nuisance = {}
    tmp_nuisance[nuisance] = nuisances_to_process[nuisance]
    postProcessNuisances(filename, samples, aliases, variables, cuts, tmp_nuisance)


