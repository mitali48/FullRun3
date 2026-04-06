#!/bin/bash

# ================= USER CONFIG =================

TAG="CR2024_noJeteEta_greaterthan_2pt5_itr1"

BASE_DIR="/eos/user/m/misharma/mkShapesRDF_rootfiles/WW2024_test/ControlRegion2024/${TAG}/rootFile"
OUTPUT_DIR="${BASE_DIR}/merged"
FINAL_OUTPUT="${BASE_DIR}/mkShapes__${TAG}.root"

NTHREADS=10

# ==============================================

mkdir -p ${OUTPUT_DIR}
cd ${BASE_DIR} || exit 1

echo " Working in: ${BASE_DIR}"
echo " Intermediate files: ${OUTPUT_DIR}"
echo ""

# ================= STEP 1 =================

echo "🔹 Detecting samples..."

SAMPLES=$(ls mkShapes__${TAG}__ALL__*.root 2>/dev/null \
    | sed "s/mkShapes__${TAG}__ALL__//" \
    | sed 's/_[0-9]*\.root//' \
    | sort | uniq)

if [ -z "$SAMPLES" ]; then
echo " No input files found!"
exit 1
fi

echo "Found samples:"
echo "$SAMPLES"
echo ""

# ================= STEP 2 =================

echo "🔹 Merging per sample..."

for SAMPLE in $SAMPLES; do
SAMPLE_OUT="${OUTPUT_DIR}/mkShapes__${TAG}__${SAMPLE}.root"
FILELIST="${OUTPUT_DIR}/${SAMPLE}_files.txt"


# Skip if already merged
if [ -f "$SAMPLE_OUT" ]; then
    echo "Skipping ${SAMPLE} (already exists)"
    continue
fi

echo "Processing ${SAMPLE}"

# Create file list
ls mkShapes__${TAG}__ALL__${SAMPLE}_*.root > ${FILELIST}

# Merge
hadd2 -j ${NTHREADS} -f ${SAMPLE_OUT} @${FILELIST}

# Check success
if [ $? -ne 0 ]; then
    echo "Error merging ${SAMPLE}"
else
    echo "Done ${SAMPLE}"
fi

echo ""

done

# ================= STEP 3 =================

echo "🔹 Final merge..."

ls ${OUTPUT_DIR}/mkShapes__${TAG}__*.root > ${OUTPUT_DIR}/all_samples.txt

hadd2 -j ${NTHREADS} -f ${FINAL_OUTPUT} @${OUTPUT_DIR}/all_samples.txt

if [ $? -ne 0 ]; then
echo " Final merge failed"
else
echo " Final file created:"
echo "${FINAL_OUTPUT}"
fi
