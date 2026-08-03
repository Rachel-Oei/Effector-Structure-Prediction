#!/bin/bash

# This script uses GPU 1. Runs ESMFOLD for each protein and appends runtime in a .csv file. 

FASTA_DIR=/home/rachel/07_fold_all/effector_p/single_cut_fasta
OUT_DIR=/linuxhome/tmp/rachel/esmfold-results
LOG_DIR=/linuxhome/tmp/rachel/esmfold-logs
ESMFOLD=/home/jankees-esmfold-103/esmfold-1.0.3/run_esmfold.sh

#After folding, copy the output to your own home directory files: 
HOME_DIR=/home/rachel/07_fold_all/effector_p/esm
RUNTIME_CSV="${HOME_DIR}/esm_runtime.csv"

#Loop through annotations for group names 
ANNOTATIONS="/home/rachel/07_fold_all/effector_p/annotations"

N_FILES=3

mkdir -p "$HOME_DIR/esmfold-results"
mkdir -p "$HOME_DIR/esmfold-logs"

for annotation in "$ANNOTATIONS"/*.txt; do

    # Get group name from annotation filename
    group=$(basename "$annotation" .txt)

    # Find FASTA files belonging to this group
    fastas=$(find "$FASTA_DIR" -maxdepth 1 -name "${group}_*.fasta" | head -n "$N_FILES")

    if [ -n "$fastas" ]; then
        
        while IFS= read -r fasta; do

            name=$(basename "$fasta" .fasta)

            echo "Group: $group"
            echo "Folding: $fasta"
            
            output_folder="${HOME_DIR}/esmfold-results/${name}"

            # Skip if ESMFolder already exists
            if [ -r "${output_folder}" ]; then
                echo "Skipping ${name}: already completed"
                continue
            fi

            echo "Running ESMFold on ${name}"

            mkdir -p "${OUT_DIR}/${name}"
            mkdir -p "${LOG_DIR}"

            # collect the runtime times 
            start=$(date +%s)

            # Run on GPU 1 
            CUDA_VISIBLE_DEVICES=1 ${ESMFOLD} \
            "$fasta" \
            "${OUT_DIR}/${name}/" \
            |& tee "${LOG_DIR}/${name}.log"

            end=$(date +%s)
            runtime=$((end - start))

            echo "Finished ${name}"
            
            echo "${name},${runtime}" >> $RUNTIME_CSV

            cp -r "${OUT_DIR}/${name}" "$HOME_DIR/esmfold-results"
            cp "${LOG_DIR}/${name}.log" "$HOME_DIR/esmfold-logs"
        
        done <<< "$fastas"

    else
        echo "WARNING: No FASTA found for group ${group}"
    fi

done
