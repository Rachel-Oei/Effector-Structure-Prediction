#!/bin/bash

# CREATES TOO MANY FOLDERS, BOTH 1FN8 AND 1FN8_1 ETC. FIX (in download_cif.py)
FASTA_DIR=/home/rachel/cif/cif_fasta
OUT_DIR=/linuxhome/tmp/rachel/esmfold-results
LOG_DIR=/linuxhome/tmp/rachel/esmfold-logs

ESMFOLD=/home/jankees-esmfold-103/esmfold-1.0.3/run_esmfold.sh

for fasta in ${FASTA_DIR}/*.fasta
do
    name=$(basename "$fasta" .fasta)

    output_folder="${OUT_DIR}/${name}"

    # Skip if ESMFolder already exists
    if [ -d "$output_folder" ]; then
        echo "Skipping ${name}: already completed"
        continue
    fi

    echo "Running ESMFold on ${name}"

    mkdir -p "${OUT_DIR}/${name}"
    mkdir -p "${LOG_DIR}"

    # Run on GPU 1 
    CUDA_VISIBLE_DEVICES=1 ${ESMFOLD} \
    "$fasta" \
    "${OUT_DIR}/${name}/" \
    |& tee "${LOG_DIR}/${name}.log"

done