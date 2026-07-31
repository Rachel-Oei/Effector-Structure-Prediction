#!/bin/bash

# This script uses GPU 0. Runs ESMFOLD for each protein and appends runtime in a .csv file. 

FASTA_DIR=/home/rachel/07_fold_all/foec_2/single_cut_fasta
OUT_DIR=/linuxhome/tmp/rachel/esmfold-results-foec2
LOG_DIR=/linuxhome/tmp/rachel/esmfold-logs-foec2
ESMFOLD=/home/jankees-esmfold-103/esmfold-1.0.3/run_esmfold.sh

#After folding, copy the output to your own home directory files: 
HOME_DIR=/home/rachel/07_fold_all/foec_2/esm
RUNTIME_CSV="${HOME_DIR}/esm_runtime.csv"

#Loop through annotations for group names 
ANNOTATIONS="/home/rachel/07_fold_all/foec_2/multi_fasta"

mkdir -p "$HOME_DIR/esmfold-results"
mkdir -p "$HOME_DIR/esmfold-logs"

for annotation in "$ANNOTATIONS"/*_08_putative_effectors_protein.fasta; do

    # Get group name from annotation filename
    group=$(basename "$annotation" _08_putative_effectors_protein.fasta)

    # Find FASTA files belonging to this group
    fasta=$(find "$FASTA_DIR" -maxdepth 1 -name "${group}_*.fasta" | head -n 1)

    if [ -n "$fasta" ]; then
        
        name=$(basename "$fasta" .fasta)

        echo "Group: $group"
        echo "Folding: $fasta"
        
        output_folder="${OUT_DIR}/${name}"

        # Skip if ESMFolder already exists
        if [ -f "${output_folder}/${name}.pdb" ]; then
            echo "Skipping ${name}: already completed"
            continue
        fi

        echo "Running ESMFold on ${name}"

        mkdir -p "${OUT_DIR}/${name}"
        mkdir -p "${LOG_DIR}"

        # collect the runtime times 
        start=$(date +%s)

        # Run on GPU 1 
        CUDA_VISIBLE_DEVICES=0 ${ESMFOLD} \
        "$fasta" \
        "${OUT_DIR}/${name}/" \
        |& tee "${LOG_DIR}/${name}.log"

        end=$(date +%s)
        runtime=$((end - start))

        echo "Finished ${name}"
        
        echo "${name},${runtime}" >> $RUNTIME_CSV

        cp -r "${OUT_DIR}/${name}" "$HOME_DIR/esmfold-results"
        cp "${LOG_DIR}/${name}.log" "$HOME_DIR/esmfold-logs"
        
    else
        echo "WARNING: No FASTA found for group ${group}"
    fi

done
