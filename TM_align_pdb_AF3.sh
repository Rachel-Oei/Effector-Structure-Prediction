#!/bin/bash

# Download through wget https://zhanggroup.org/TM-align/TMalign.cpp
# Compile through g++ -O3 -ffast-math -lm -o TMalign TMalign.cpp
# I have the 2022 version, could not find the 2024 version. 

# Paths
EXPERIMENTAL=~/TM-align/clean_pdbs
PREDICTED=/home/rachel/alphafold3-3.0.3/output
OUTDIR=~/TM-align/results2

mkdir -p "$OUTDIR"

# Loop through AF3 folders
for folder in "$PREDICTED"/*; do

    # Get folder name (example: 2MYW_1)
    id=$(basename "$folder")

    predicted="$PREDICTED/${id}/${id}_model.cif"
    experimental="$EXPERIMENTAL/${id}.pdb"

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