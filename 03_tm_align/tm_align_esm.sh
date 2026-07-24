#!/bin/bash

# Download through wget https://zhanggroup.org/TM-align/TMalign.cpp
# Compile through g++ -O3 -ffast-math -lm -o TMalign TMalign.cpp
# I have the 2022 version, could not find the 2024 version. 

# Paths
HOME="/home/rachel"
EXPERIMENTAL="${HOME}/01_prepare_cif/cif_single_chain"
PREDICTED="${HOME}/02_folding/esm/esmfold-results"
OUTDIR="${HOME}/03_tm_align/results_esm"

mkdir -p "$OUTDIR"

# Loop through ESMFold folders
for folder in "$PREDICTED"/*; do

    # Get folder name (example: 2MYW_1)
    id=$(basename "$folder")

    predicted=$(find "$folder" -maxdepth 1 -name "*.pdb" | head -n 1)
    experimental="$EXPERIMENTAL/${id}.cif"

    echo "====================================="
    echo "Structure: $id"

    echo "Predicted: $predicted"
    echo "Experimental: $experimental"

    # Run TM-align
    TMalign "$predicted" "$experimental" \
        > "$OUTDIR/${id}_tmalign.txt"

    echo "Completed $id"

done

echo "Finished all TM-align comparisons."