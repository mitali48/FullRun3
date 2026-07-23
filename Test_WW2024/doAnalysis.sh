#!/bin/bash
echo ""
echo "Prepare input cards!"
echo ""

cd /eos/user/m/misharma/private/Latinos/HWWRun3/CMSSW_14_1_0_pre4/src

cmsenv

ulimit -Ss unlimited

combineTool.py  -M Impacts -d 0j_all.root -m 125 -n Test --doInitialFit   -t -1  --expectSignal  1

combineTool.py  -M Impacts -d 0j_all.root -m 125 -n Test --doFit   -t -1  --expectSignal  1 --job-mode=interactive --parallel=10
 

combineTool.py  -M Impacts -d 0j_all.root -m 125 -n Test  --output  name.json -t -1  --expectSignal  1 

plotImpacts.py -i impacts.json -o impacts 