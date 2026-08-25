#!/bin/bash

# Uses GPU 0. Uses setup of another user (jan kees).
MODEL_DIR="/home/rachel/07_fold_all/foec_2/af2/alphafold-2.3.2"
OUTPUT_DIR="${MODEL_DIR}/output/results"
LOG_DIR="${MODEL_DIR}/output/logs"
RUNTIME_CSV="/home/rachel/07_fold_all/foec_2/af2/af2_runtime.csv"
FASTA_DIR="/home/rachel/07_fold_all/foec_2/select_separate_fasta"

mkdir -p ${MODEL_DIR}
mkdir -p ${OUTPUT_DIR}
mkdir -p ${LOG_DIR}

for fasta in "${FASTA_DIR}"/*.fasta 
do

    protein_identity=$(basename "$fasta" .fasta)

    ranked_file="${OUTPUT_DIR}/${protein_identity}/ranked_0.pdb"

    # Skip if AF2 output already exists
    if [ -f "$ranked_file" ]; then
        echo "Skipping ${protein_identity}: already completed"
        continue
    fi

    # Everytime it runs, create a touch file. 
    # So that another process cannot run it at the same time.

    touch_file="${OUTPUT_DIR}/${protein_identity}.running"

    if [ -f "$touch_file" ]; then
    echo "Skipping ${protein_identity}: another process is running"
    continue
    fi

    touch "$touch_file"

    start=$(date +%s)

    # Uses GPU 0. The "0" specifies GPU
    /home/jankees-alphafold-232/alphafold-2.3.2/run_alphafold.sh \
    -d /net/leca/linuxhome/alphafold/alphafold-db-2.3.2 \
    -o "${OUTPUT_DIR}" \
    -f "${fasta}" \
    -a 0 \
    -t 2020-05-14 2>&1 | tee "${LOG_DIR}/${protein_identity}.log"

    end=$(date +%s)
    runtime=$((end - start))

    echo "${protein_identity},${runtime}" >> $RUNTIME_CSV

    # Remove the touch file at the end 
    rm -f "$touch_file"
done 