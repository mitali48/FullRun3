set -euo pipefail

CMSSW_BASE="/eos/user/m/misharma/private/Latinos/HWWRun3/CMSSW_14_1_0_pre4/src"

CARDDIR="/eos/user/m/misharma/mkShapesRDF_rootfiles/FullRun3/Full2024v15/njets/Itr5_bReq20GeV_Iv2/datacards"

cd "${CMSSW_BASE}"

cmsenv

ulimit -Ss unlimited

cd "${CARDDIR}"

# combineCards.py \
#     SR0j=SR_0j/events/datacard.txt \
#     Top_bReq1_0j=TopCR_bReq1_0j/events/datacard.txt \
#     Top_bReq2_0j=TopCR_bReq2_0j/events/datacard.txt \
#     DY0j=DYtautauCR_0j/events/datacard.txt \
#     Fake_0j=nonpromptCR_0j/events/datacard.txt \
#     > combined_0j.txt


# combineCards.py \
#     SR1j=SR_1j/events/datacard.txt \
#     Top_bReq1_1j=TopCR_bReq1_1j/events/datacard.txt \
#     Top_bReq2_1j=TopCR_bReq2_1j/events/datacard.txt \
#     DY1j=DYtautauCR_1j/events/datacard.txt \
#     Fake_1j=nonpromptCR_1j/events/datacard.txt \
#     > combined_1j.txt


# combineCards.py \
#     SR2j=SR_maj2j/events/datacard.txt \
#     Top_bReq1_2j=TopCR_bReq1_maj2j/events/datacard.txt \
#     Top_bReq2_2j=TopCR_bReq2_maj2j/events/datacard.txt \
#     DY2j=DYtautauCR_maj2j/events/datacard.txt \
#     Fake_2j=nonpromptCR_maj2j/events/datacard.txt \
#     > combined_2j.txt

# combineCards.py \
#     combined_0j.txt \
#     combined_1j.txt \
#     combined_2j.txt \
#     > datacard_fiducial.txt

text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
    -m 125 \
    datacard_fiducial.txt \
    --PO verbose \
    --PO 'map=.*/WW_B0:r0[1,0,3]' \
    --PO 'map=.*/WW_B1:r1[1,0,3]' \
    --PO 'map=.*/WW_B2:r2[1,0,3]' \
    --PO 'map=.*/ggWW_B0:r0[1,0,3]' \
    --PO 'map=.*/ggWW_B1:r1[1,0,3]' \
    --PO 'map=.*/ggWW_B2:r2[1,0,3]' \
    -o workspace_fiducial.root

combine -M MultiDimFit workspace_fiducial.root \
    --algo=singles \
    --robustFit=1 \
    --X-rtd FITTER_DYN_STEP \
    --redefineSignalPOIs r0,r1,r2 \
    --setParameters r0=1,r1=1,r2=1 \
    --setParameterRanges r0=0.8,1.2:r1=0.8,1.2:r2=0.8,1.2 \
    -t -1

# Common options
COMMON="-d workspace_fiducial.root -m 125 -n JetBins \
  --redefineSignalPOIs r0,r1,r2 \
  --setParameters r0=1,r1=1,r2=1 \
  --setParameterRanges r0=0.8,1.2:r1=0.8,1.2:r2=0.8,1.2 \
  --cminDefaultMinimizerStrategy 2 --cminDefaultMinimizerTolerance 0.01
  -t -1 --robustFit 1"

# 1. Initial fit (all three POIs simultaneously)
combineTool.py -M Impacts $COMMON --doInitialFit

# 2. Fit for each nuisance parameter
combineTool.py -M Impacts $COMMON --doFits \
    --job-mode interactive --parallel 10

# 3. Collect into JSON (contains impacts for r0, r1, r2)
combineTool.py -M Impacts $COMMON --output impacts_jetbins.json

# 4. One plot per POI
for poi in r0 r1 r2; do
  plotImpacts.py -i impacts_jetbins.json -o impacts_jetbins_${poi} --POI ${poi}
done


# combineTool.py -M Impacts -d workspace_fiducial.root -m 125 -n Test --doInitialFit -t -1 --expectSignal 1 --robustFit 1

# combineTool.py -M Impacts -d workspace_fiducial.root -m 125 -n Test --doFit -t -1 --expectSignal 1  --robustFit 1 --job-mode=interactive --parallel=10


# combineTool.py -M Impacts -d workspace_fiducial.root -m 125 -n Test --output json_inclusive.json  -t -1 --expectSignal 1 --robustFit 1


# plotImpacts.py -i json_inclusive.json -o impacts_inclusive


#  combine -M MultiDimFit workspace_ww.root -n ww_incl_exp --algo=singles --robustFit=1 --X-rtd FITTER_DYN_STEP  --redefineSignalPOIs r_s0 --setParameterRanges r_s0=0.6,1.8 --setParameters r_s0=1 -t -1

# text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
#     -m 125 \
#     datacard_fiducial.txt \
#     --PO verbose \
#     --PO 'map=.*/WW_B0:r0[1,0,3]' \
#     --PO 'map=.*/WW_B1:r1[1,0,3]' \
#     --PO 'map=.*/WW_B2:r2[1,0,3]' \
#     --PO 'map=.*/WW_B3:r3[1,0,3]' \
#     --PO 'map=.*/ggWW_B0:r0[1,0,3]' \
#     --PO 'map=.*/ggWW_B1:r1[1,0,3]' \
#     --PO 'map=.*/ggWW_B2:r2[1,0,3]' \
#     --PO 'map=.*/ggWW_B3:r3[1,0,3]' \
#     -o workspace_fiducial.root

# combine -M MultiDimFit workspace_fiducial.root \
#     --algo=singles \
#     --robustFit=1 \
#     --X-rtd FITTER_DYN_STEP \
#     --redefineSignalPOIs r0,r1,r2,r3 \
#     --setParameters r0=1,r1=1,r2=1,r3=1 \
#     --setParameterRanges r0=0.1,10:r1=0.1,10:r2=0.2,10:r3=0.1,10 \
#     -t -1



# combineCards.py \
#     SR0j=SR_0j/events/datacard.txt \
#     SR1j=SR_1j/events/datacard.txt \
#     SR2j=SR_maj2j/events/datacard.txt \
#     > combined_SR.txt

# text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel datacard_njets.txt\
#     --PO 'map=.*/WW_B0:r0[1,0,3]' \
#     --PO 'map=.*/WW_B1:r1[1,0,3]' \
#     --PO 'map=.*/WW_B2:r2[1,0,3]' \
#     --PO 'map=.*/WW_B3:r3[1,0,3]' \
#     --PO 'map=.*/ggWW_B0:r0[1,0,3]' \
#     --PO 'map=.*/ggWW_B1:r1[1,0,3]' \
#     --PO 'map=.*/ggWW_B2:r2[1,0,3]' \
#     --PO 'map=.*/ggWW_B3:r3[1,0,3]' \
#     -o workspace_njets.root


# text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel combined_SR.txt\
#     --PO 'map=.*/WW_B0:r0[1,0,3]' \
#     --PO 'map=.*/WW_B1:r1[1,0,3]' \
#     --PO 'map=.*/WW_B2:r2[1,0,3]' \
#     --PO 'map=.*/WW_B3:r3[1,0,3]' \
#     --PO 'map=.*/ggWW_B0:r0[1,0,3]' \
#     --PO 'map=.*/ggWW_B1:r1[1,0,3]' \
#     --PO 'map=.*/ggWW_B2:r2[1,0,3]' \
#     --PO 'map=.*/ggWW_B3:r3[1,0,3]' \
#     -o workspace_SR.root


# text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel combined_SR.txt\
#     --PO 'map=.*/WW_B0:r0[1,0,3]' \
#     --PO 'map=.*/WW_B1:r1[1,0,3]' \
#     --PO 'map=.*/WW_B2:r2[1,0,3]' \
#     --PO 'map=.*/ggWW_B0:r0[1,0,3]' \
#     --PO 'map=.*/ggWW_B1:r1[1,0,3]' \
#     --PO 'map=.*/ggWW_B2:r2[1,0,3]' \
#     -o workspace_SR_3par.root


# combineTool.py -M Impacts \
#   -d workspace_njets.root \
#   -m 125 \
#   --redefineSignalPOIs r0,r1,r2,r3 \
#   -t -1 \
#   --setParameters r0=1,r1=1,r2=1,r3=1 \
#   --setParameterRanges r0=0,3:r1=0,3:r2=0,3:r3=0 \
#   --doInitialFit \
#   --robustFit 1

# combine -M MultiDimFit \
#     workspace_SR_3par.root \
#     -t -1 \
#     --setParameters r0=1,r1=1,r2=1 \
#     --setParameterRanges r0=0,5:r1=0,5:r2=0,5 \
#     -m 125 \
#     -v 3