#!/bin/bash

# Download through wget https://zhanggroup.org/TM-align/TMalign.cpp
# Compile through g++ -O3 -ffast-math -lm -o TMalign TMalign.cpp
# I have the 2022 version, could not find the 2024 version. 

# Paths
HOME="/home/rachel"
EXPERIMENTAL="${HOME}/01_prepare_cif/cif_single_chain"
PREDICTED="${HOME}/02_folding/af2/alphafold-2.3.2/output"
OUTDIR="${HOME}/03_tm_align/results_af2"

mkdir -p "$OUTDIR"

# Loop through AF2 folders
for folder in "$PREDICTED"/*; do

    # Get folder name (example: 2MYW_1)
    id=$(basename "$folder")

    predicted="$PREDICTED/${id}/ranked_0.pdb"
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