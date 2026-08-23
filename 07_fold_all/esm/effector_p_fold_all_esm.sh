#!/bin/bash

# This script uses GPU 1. Runs ESMFOLD for each protein and appends runtime in a .csv file. 

FASTA_DIR=/home/rachel/07_fold_all/effector_p/select_separate_fasta
OUT_DIR=/linuxhome/tmp/rachel/esmfold-results
LOG_DIR=/linuxhome/tmp/rachel/esmfold-logs
ESMFOLD=/home/jankees-esmfold-103/esmfold-1.0.3/run_esmfold.sh

#After folding, copy the output to your own home directory files: 
HOME_DIR=/home/rachel/07_fold_all/effector_p/esm
RUNTIME_CSV="${HOME_DIR}/esm_runtime.csv"

mkdir -p "$OUT_DIR"
mkdir -p "$LOG_DIR"
mkdir -p "$HOME_DIR/esmfold-results"
mkdir -p "$HOME_DIR/esmfold-logs"

for fasta in "$FASTA_DIR"/*.fasta; do

    filename=$(basename "$fasta" .fasta)

    echo "Folding: $filename"

    output_folder="${OUT_DIR}/${filename}"

    # Skip if ESMFold output already exists
    if [ -d "$output_folder" ]; then
        echo "Skipping ${filename}: already completed"
        continue
    fi

    mkdir -p "$output_folder"

    # Collect runtime
    start=$(date +%s)

    # Run on GPU 1
    CUDA_VISIBLE_DEVICES=1 "$ESMFOLD" \
        "$fasta" \
        "${output_folder}/" \
        |& tee "${LOG_DIR}/${filename}.log"

    end=$(date +%s)
    runtime=$((end - start))

    echo "Finished ${filename}"

    echo "${filename},${runtime}" >> "$RUNTIME_CSV"

    # Copy results to home directory
    cp -r "$output_folder" "$HOME_DIR/esmfold-results/"
    cp "${LOG_DIR}/${filename}.log" "$HOME_DIR/esmfold-logs/"

done
