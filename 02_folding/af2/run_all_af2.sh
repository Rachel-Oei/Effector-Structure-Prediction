#!/bin/bash

# Uses GPU 1. Uses setup of another user (jan kees).
MODEL_DIR="/home/rachel/02_folding/af2/alphafold-2.3.2"
OUTPUT_DIR="${MODEL_DIR}/output/results"
LOG_DIR="${MODEL_DIR}/output/logs"
RUNTIME_CSV="/home/rachel/02_folding/af2/af2_runtime.csv"

FASTA_DIR="/home/rachel/01_prepare_cif/cif_fasta"

mkdir -p ${MODEL_DIR}
mkdir -p ${OUTPUT_DIR}
mkdir -p ${LOG_DIR}

for fasta_file in ${FASTA_DIR}/*.fasta
do

    protein_identity=$(basename "$fasta_file" .fasta)

    ranked_file="${OUTPUT_DIR}/${protein_identity}/ranked_0.pdb"

    # Skip if AF2 output already exists
    if [ -f "$ranked_file" ]; then
        echo "Skipping ${protein_identity}: already completed"
        continue
    fi

    start=$(date +%s)

    # Uses GPU 1 
    /home/jankees-alphafold-232/alphafold-2.3.2/run_alphafold.sh \
    -d /net/leca/linuxhome/alphafold/alphafold-db-2.3.2 \
    -o ${OUTPUT_DIR} \
    -f ${fasta_file} -a 1 -t 2020-05-14 \
    |& tee "${LOG_DIR}/${protein_identity}.log"

    end=$(date +%s)
    runtime=$((end - start))

    echo "${protein_identity},${runtime}" >> $RUNTIME_CSV

done 