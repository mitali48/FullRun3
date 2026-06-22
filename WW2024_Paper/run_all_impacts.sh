#!/bin/bash

set -euo pipefail

echo "========================================"
echo " Setting up Combine environment"
echo "========================================"

CMSSW_BASE=/eos/user/m/misharma/private/Latinos/HWWRun3/CMSSW_14_1_0_pre4/src
CARDDIR=/eos/user/m/misharma/mkShapesRDF_rootfiles/WW2024_Paper/SR_CR_nuisances/Itr6_bReq2_1or2/datacards

cd ${CMSSW_BASE}
cmsenv

ulimit -Ss unlimited

cd ${CARDDIR}

###########################################################

# Function to run impacts for a workspace

###########################################################

runImpacts() {

local WORKSPACE=$1
local TAG=$2

echo ""
echo "========================================"
echo " Running impacts for ${TAG}"
echo "========================================"

rm -rf impacts_${TAG}
mkdir -p impacts_${TAG}

cp ${WORKSPACE} impacts_${TAG}/workspace.root

cd impacts_${TAG}

echo "---- FitDiagnostics ----"

combine -M FitDiagnostics \
    workspace.root \
    -m 125 \
    -t -1 \
    --expectSignal 1 \
    --rMin 0 \
    --rMax 5 \
    --saveShapes \
    --saveWithUncertainties \
    --saveNormalizations \
    2>&1 | tee fitDiagnostics.log

echo "---- Initial Fit ----"

combineTool.py -M Impacts \
    -d workspace.root \
    -m 125 \
    --doInitialFit \
    -t -1 \
    --expectSignal 1 \
    --rMin 0 \
    --rMax 5 \
    --robustFit 1 \
    2>&1 | tee impacts_initialFit.log

echo "---- Nuisance Fits ----"

combineTool.py -M Impacts \
    -d workspace.root \
    -m 125 \
    --doFits \
    -t -1 \
    --expectSignal 1 \
    --rMin 0 \
    --rMax 5 \
    --robustFit 1 \
    --parallel 10 \
    2>&1 | tee impacts_fits.log

echo "---- Collect Impacts ----"

combineTool.py -M Impacts \
    -d workspace.root \
    -m 125 \
    -o impacts.json

echo "---- Plot Impacts ----"

plotImpacts.py \
    -i impacts.json \
    -o impacts

echo "---- Best-fit signal strength ----"

combine -M MultiDimFit \
    workspace.root \
    -m 125 \
    --redefineSignalPOIs r \
    --algo singles \
    -t -1 \
    --expectSignal 1 \
    --rMin 0 \
    --rMax 5 \
    2>&1 | tee multidimfit.log

cd ..

echo "Finished ${TAG}"

}

###########################################################

# Build category cards

###########################################################

# echo "========================================"
# echo " Building category cards"
# echo "========================================"

# combineCards.py \
#     SR0j=SR_0j/events/datacard.txt \
#     Top0j=Top_CR_0j/events/datacard.txt \
#     DY0j=DYtautauCR_0j/events/datacard.txt \
#     Fake0j=nonpromptCR_0j/events/datacard.txt \
#     > combined_0j.txt

# combineCards.py \
#     SR1j=SR_1j/events/datacard.txt \
#     Top1j=Top_CR_1j/events/datacard.txt \
#     DY1j=DYtautauCR_1j/events/datacard.txt \
#     Fake1j=nonpromptCR_1j/events/datacard.txt \
#     > combined_1j.txt

# combineCards.py \
#     SR2j=SR_2j/events/datacard.txt \
#     Top2j=Top_CR_2j/events/datacard.txt \
#     DY2j=DYtautauCR_2j/events/datacard.txt \
#     Fake2j=nonpromptCR_2j/events/datacard.txt \
#     > combined_2j.txt

# combineCards.py \
#     SR3j=SR_3j/events/datacard.txt \
#     Top3j=Top_CR_3j/events/datacard.txt \
#     DY3j=DYtautauCR_3j/events/datacard.txt \
#     Fake3j=nonpromptCR_3j/events/datacard.txt \
#     > combined_3j.txt

# combineCards.py \
#     SRInc=SR_Inc/events/datacard.txt \
#     TopInc=Top_CR_Inc/events/datacard.txt \
#     DYInc=DYtautauCR_Inc/events/datacard.txt \
#     FakeInc=nonpromptCR_Inc/events/datacard.txt \
#     > combined_inc.txt

# combineCards.py \
#     Cat0j=combined_0j.txt \
#     Cat1j=combined_1j.txt \
#     Cat2j=combined_2j.txt \
#     Cat3j=combined_3j.txt \
#     > combined.txt

###########################################################

# Create workspaces

###########################################################

# echo "========================================"
# echo " Creating workspaces"
# echo "========================================"

text2workspace.py combined_0j.txt  -m 125 -o workspace_0j.root
text2workspace.py combined_1j.txt  -m 125 -o workspace_1j.root
text2workspace.py combined_2j.txt  -m 125 -o workspace_2j.root
text2workspace.py combined_3j.txt  -m 125 -o workspace_3j.root
text2workspace.py combined_inc.txt -m 125 -o workspace_inc.root
text2workspace.py combined.txt     -m 125 -o workspace_combined.root

# ###########################################################

# # Run impacts

# ###########################################################

runImpacts workspace_0j.root  0j
runImpacts workspace_1j.root  1j
runImpacts workspace_2j.root  2j
runImpacts workspace_3j.root  3j
runImpacts workspace_inc.root Inc
runImpacts workspace_combined.root Combined

echo ""
echo "========================================"
echo " All categories completed"
echo "========================================"

echo ""
echo "Results:"
echo "  impacts_0j/impacts.pdf"
echo "  impacts_1j/impacts.pdf"
echo "  impacts_2j/impacts.pdf"
echo "  impacts_3j/impacts.pdf"
echo "  impacts_Inc/impacts.pdf"
echo "  impacts_Combined/impacts.pdf"
