#!/bin/bash

BASE="/eos/user/m/misharma/mkShapesRDF_rootfiles/LeptonID_optimization/nominal_SR_CR__ele_Run3__mu_pfLooseID_HWW_tthmva_67/datacards"

regions=("sr" "top" "ss" "dytt")
jets=("0j" "1j" "2j" "Inc")

# detect variables
ref_dir="${BASE}/ww2l2v_sr_0j"

if [ ! -d "$ref_dir" ]; then
  echo "❌ ERROR: Directory not found: $ref_dir"
  exit 1
fi

variables=($(ls "$ref_dir"))

echo "Variables found:"
echo "${variables[@]}"

mkdir -p ${BASE}/combined

########################################
# Combine regions per jet + variable
########################################

for jet in "${jets[@]}"; do
  echo "========================"
  echo "Processing jet: $jet"
  echo "========================"

  for var in "${variables[@]}"; do

    cmd="combineCards.py"

    for reg in "${regions[@]}"; do
      card="${BASE}/ww2l2v_${reg}_${jet}/${var}/datacard.txt"

      if [ -f "$card" ]; then
        cmd="$cmd ${reg}=${card}"
      else
        echo "⚠️ Missing: $card"
      fi
    done

    out="${BASE}/combined/datacard_${var}_${jet}.txt"
    echo "➡️ Creating $out"

    eval "$cmd > $out"

  done
done

echo "✅ All combinations done!"