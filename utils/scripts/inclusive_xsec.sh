#!/bin/bash
set -euo pipefail

CMSSW_BASE="/eos/user/m/misharma/private/Latinos/HWWRun3/CMSSW_14_1_0_pre4/src"

CARDDIR="/eos/user/m/misharma/mkShapesRDF_rootfiles/FullRun3/Full2022EEv12/Inclusive/Itr0_bReq20/datacards"

cd "${CMSSW_BASE}"

cmsenv

ulimit -Ss unlimited

cd "${CARDDIR}"


combineCards.py \
    SR0j=SR_0j/events/datacard.txt \
    Top_bReq1_0j=TopCR_bReq1_0j/events/datacard.txt \
    Top_bReq2_0j=TopCR_bReq2_0j/events/datacard.txt \
    DY0j=DYtautauCR_0j/events/datacard.txt \
    > combined_0j.txt


combineCards.py \
    SR1j=SR_1j/events/datacard.txt \
    Top_bReq1_1j=TopCR_bReq1_1j/events/datacard.txt \
    Top_bReq2_1j=TopCR_bReq2_1j/events/datacard.txt \
    DY1j=DYtautauCR_1j/events/datacard.txt \
    Fake_1j=nonpromptCR_1j/events/datacard.txt \
    > combined_1j.txt


combineCards.py \
    SR2j=SR_maj2j/events/datacard.txt \
    Top_bReq1_2j=TopCR_bReq1_maj2j/events/datacard.txt \
    Top_bReq2_2j=TopCR_bReq2_maj2j/events/datacard.txt \
    DY2j=DYtautauCR_maj2j/events/datacard.txt \
    Fake_2j=nonpromptCR_maj2j/events/datacard.txt \
    > combined_2j.txt

# combineCards.py \
#     combined_0j.txt \
#     combined_1j.txt \
#     combined_2j.txt \
#     > datacard_inclusive.txt


# text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
#   --PO verbose \
#   --PO 'map=.*/WW:r[1,0,3]' \
#   --PO 'map=.*/ggWW:r[1,0,3]' \
#   combined_0j.txt \
#   -o workspace_0j.root

# combine -M MultiDimFit workspace_0j.root \
#     --algo=singles \
#     --robustFit=1  \
#     --redefineSignalPOIs r \
#     --setParameters r=1 \
#     --setParameterRanges r=0.8,1.2 \
#     -t -1 \

# text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
#   --PO verbose \
#   --PO 'map=.*/WW:r[1,0,3]' \
#   --PO 'map=.*/ggWW:r[1,0,3]' \
#   combined_1j.txt \
#   -o workspace_1j.root

# combine -M MultiDimFit workspace_1j.root \
#     --algo=singles \
#     --robustFit=1  \
#     --redefineSignalPOIs r \
#     --setParameters r=1 \
#     --setParameterRanges r=0.1,10. \
#     -t -1 \

# text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
#   --PO verbose \
#   --PO 'map=.*/WW:r[1,0,3]' \
#   --PO 'map=.*/ggWW:r[1,0,3]' \
#   combined_2j.txt \
#   -o workspace_2j.root

# combine -M MultiDimFit workspace_2j.root \
#     --algo=singles \
#     --robustFit=1  \
#     --redefineSignalPOIs r \
#     --setParameters r=1 \
#     --setParameterRanges r=0.1,10. \
#     -t -1 \


text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
  --PO verbose \
  --PO 'map=.*/WW:r[1,0,3]' \
  --PO 'map=.*/ggWW:r[1,0,3]' \
  datacard_inclusive.txt \
  -o workspace_inclusive.root

combine -M MultiDimFit workspace_inclusive.root \
    --algo=singles \
    --robustFit=1  \
    --redefineSignalPOIs r \
    --setParameters r=1 \
    --setParameterRanges r=0.8,1.2 \
    -t -1 \


combineTool.py -M Impacts -d workspace_inclusive.root -m 125 -n Test --doInitialFit -t -1 --expectSignal 1 --robustFit 1

combineTool.py -M Impacts -d workspace_inclusive.root -m 125 -n Test --doFit -t -1 --expectSignal 1  --robustFit 1 --job-mode=interactive --parallel=10


combineTool.py -M Impacts -d workspace_inclusive.root -m 125 -n Test --output json_inclusive.json  -t -1 --expectSignal 1 --robustFit 1


plotImpacts.py -i json_inclusive.json -o impacts_inclusive

