#!/bin/bash

FASTA_DIR=/home/rachel/01_prepare_cif/cif_fasta
OUT_DIR=/linuxhome/tmp/rachel/esmfold-results
LOG_DIR=/linuxhome/tmp/rachel/esmfold-logs
ESMFOLD=/home/jankees-esmfold-103/esmfold-1.0.3/run_esmfold.sh

#After folding, copy the output to your own home directory files: 
HOME_DIR=/home/rachel/02_folding/esm

for fasta in ${FASTA_DIR}/*.fasta
do
    name=$(basename "$fasta" .fasta)

    output_folder="${OUT_DIR}/${name}"

    # Skip if ESMFolder already exists
    if [ -f "${output_folder}/${name}.pdb" ]; then
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

cp -r "$OUT_DIR" "$HOME_DIR"
cp -r "$LOG_DIR" "$HOME_DIR"
