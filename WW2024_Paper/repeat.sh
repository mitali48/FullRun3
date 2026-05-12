#!/bin/bash

if [ $# -eq 0 ]; then
	echo "$0: Missing arguments"
	exit 1
else
	echo "We got some argument(s)"
	echo "==========================="
	echo "Number of arguments. : $#"
	echo "List of arguments... : $@"
	echo "Arg #1: sample       : $1"
	echo "Arg #2: compile      : $2"
	echo "==========================="
	SAMPLE=$1
	COMPILE=$2
fi


if [ "$COMPILE" == "True" ]; then
	mkShapesRDF -c 1
	mkShapesRDF -o 0 -f . -b 1 -dR 1
fi

# cd /afs/cern.ch/user/m/misharma/private/Latinos/HWWRUn3/PlotsConfigurationsRun3/WW_Run3/MyPlotsConfiguration/Test_WW2024/eos/user/m/misharma/mkShapesRDF_rootfiles/WW2024/test28Jan2026/condor/WW2024_test
# cd condor/EGamma1_Run2024I-Prompt-v1/${SAMPLE}/
cd condor/Itr4_Old_evaluate_btag/${SAMPLE}/
cp /eos/user/m/misharma/private/Latinos/HWWRun3/mkShapesRDF/mkShapesRDF/include/headers.hh /eos/user/m/misharma/private/Latinos/HWWRun3/mkShapesRDF/mkShapesRDF/shapeAnalysis/runner.py   .
python runner.py
cp output.root /eos/user/m/misharma/mkShapesRDF_rootfiles/WW2024_Paper/rootFiles__ALL__${SAMPLE}.root
# cp output.root /afs/cern.ch/user/m/misharma/private/Latinos/HWWRUn3/PlotsConfigurationsRun3/WW_Run3/rootFiles__ALL__${SAMPLE}.root
#cp /afs/cern.ch/user/m/misharma/private/Latinos/HWWRUn3/PlotsConfigurationsRun3/WW_Run3/FullRun3/2022/rootFiles/rootFiles__ALL__${SAMPLE}.root
rm output.root
