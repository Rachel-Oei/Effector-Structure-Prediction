#!/bin/bash

# The script is executed with either "effector_p" or "foec_2" as the first option.
# Second option specifies the gpu, so "0" or "1".
# Example: bash fold_reference_esm.sh foec_2 1

PIPELINE="$1"
GPU="$2"

# Check whether pipeline is correct 
if [[ "$PIPELINE" != "effector_p" && "$PIPELINE" != "foec_2" ]]; then
    echo "Error: pipeline must be 'effector_p' or 'foec_2'"
    exit 1
fi

if [[ "$GPU" != "0" && "$GPU" != "1" ]]; then
    echo "Error: GPU must be '0' or '1'"
    exit 1
fi

FASTA_DIR="/home/rachel/09_Fo4287_reference/${PIPELINE}/single_cut_fasta"
OUT_DIR="/linuxhome/tmp/rachel/09_Fo4287/${PIPELINE}/esmfold-results"
LOG_DIR="/linuxhome/tmp/rachel/09_Fo4287/${PIPELINE}/esmfold-logs"
ESMFOLD="/home/jankees-esmfold-103/esmfold-1.0.3/run_esmfold.sh"

#After folding, copy the output to your own home directory files: 
HOME_DIR="/home/rachel/09_Fo4287_reference/${PIPELINE}/esm"
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
    CUDA_VISIBLE_DEVICES=${GPU} "$ESMFOLD" \
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
