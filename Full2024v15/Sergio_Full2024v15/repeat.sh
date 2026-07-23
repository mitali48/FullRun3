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
cd condor/WW_2024/${SAMPLE}/
cp /afs/cern.ch/user/m/misharma/private/Latinos/HWWRUn3/mkShapesRDF/mkShapesRDF/include/headers.hh /afs/cern.ch/user/m/misharma/private/Latinos/HWWRUn3/mkShapesRDF/mkShapesRDF/shapeAnalysis/runner.py   .
python runner.py
cp output.root /eos/user/m/misharma/mkShapesRDF_rootfiles/WW_2024/rootFiles__ALL__${SAMPLE}.root
# cp output.root /afs/cern.ch/user/m/misharma/private/Latinos/HWWRUn3/PlotsConfigurationsRun3/WW_Run3/rootFiles__ALL__${SAMPLE}.root
#cp /afs/cern.ch/user/m/misharma/private/Latinos/HWWRUn3/PlotsConfigurationsRun3/WW_Run3/FullRun3/2022/rootFiles/rootFiles__ALL__${SAMPLE}.root
rm output.root
