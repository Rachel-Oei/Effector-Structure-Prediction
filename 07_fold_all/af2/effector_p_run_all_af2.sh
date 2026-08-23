#!/bin/bash

# Uses GPU 1. Uses setup of another user (jan kees).
MODEL_DIR="/home/rachel/07_fold_all/effector_p/af2/alphafold-2.3.2"
OUTPUT_DIR="${MODEL_DIR}/output/results"
LOG_DIR="${MODEL_DIR}/output/logs"
RUNTIME_CSV="/home/rachel/07_fold_all/effector_p/af2/af2_runtime.csv"
FASTA_DIR="/home/rachel/07_fold_all/effector_p/select_separate_fasta"

# Since the effector p pipeline contains spaces in the naming, and AF2 does not work, 
# we create a separate folder with the fastas without spaces. 
AF2_FASTA_DIR="${MODEL_DIR}/input_fasta"

mkdir -p ${MODEL_DIR}
mkdir -p ${OUTPUT_DIR}
mkdir -p ${LOG_DIR}
mkdir -p "${AF2_FASTA_DIR}"

for fasta in "${FASTA_DIR}"/*.fasta 
do

    protein_identity=$(basename "$fasta" .fasta)

    # Replace spaces with underscores for AF2 only
    af2_identity="${protein_identity// /_}"

    # Create a space-free symlink to the original FASTA
    af2_fasta="${AF2_FASTA_DIR}/${af2_identity}.fasta"
    ln -sf "$fasta" "$af2_fasta"

    ranked_file="${OUTPUT_DIR}/${af2_identity}/ranked_0.pdb"

    # Skip if AF2 output already exists
    if [ -f "$ranked_file" ]; then
        echo "Skipping ${af2_identity}: already completed"
        continue
    fi

    start=$(date +%s)

    # Uses GPU 1. The "1" specifies GPU
    /home/jankees-alphafold-232/alphafold-2.3.2/run_alphafold.sh \
        -d /net/leca/linuxhome/alphafold/alphafold-db-2.3.2 \
        -o "${OUTPUT_DIR}" \
        -f "${af2_fasta}" \
        -a 1 \
        -t 2020-05-14 2>&1 | tee "${LOG_DIR}/${af2_identity}.log"

    end=$(date +%s)
    runtime=$((end - start))

    echo "${af2_identity},${runtime}" >> "${RUNTIME_CSV}"

done