#!/bin/bash

# Uses GPU 0. Uses setup of another user (jan kees).
MODEL_DIR="/home/rachel/07_fold_all/foec_2/af2/alphafold-2.3.2"
OUTPUT_DIR="${MODEL_DIR}/output/results"
LOG_DIR="${MODEL_DIR}/output/logs"
RUNTIME_CSV="/home/rachel/07_fold_all/foec_2/af2/af2_runtime.csv"

FASTA_DIR="/home/rachel/07_fold_all/foec_2/single_cut_fasta"

ANNOTATIONS="/home/rachel/07_fold_all/foec_2/multi_fasta"

N_FILES=1 

mkdir -p ${MODEL_DIR}
mkdir -p ${OUTPUT_DIR}
mkdir -p ${LOG_DIR}

for annotation in "$ANNOTATIONS"/*_08_putative_effectors_protein.fasta; do

    # Get group name from annotation filename
    group=$(basename "$annotation" _08_putative_effectors_protein.fasta)

    # Find FASTA files belonging to this group
    fastas=$(find "$FASTA_DIR" -maxdepth 1 -name "${group}_*.fasta" | head -n "$N_FILES")

    if [ -n "$fastas" ]; then
        
        while IFS= read -r fasta; do

            protein_identity=$(basename "$fasta" .fasta)

            ranked_file="${OUTPUT_DIR}/${protein_identity}/ranked_0.pdb"

            # Skip if AF2 output already exists
            if [ -f "$ranked_file" ]; then
                echo "Skipping ${protein_identity}: already completed"
                continue
            fi

            start=$(date +%s)

            # Uses GPU 0
            /home/jankees-alphafold-232/alphafold-2.3.2/run_alphafold.sh \
            -d /net/leca/linuxhome/alphafold/alphafold-db-2.3.2 \
            -o ${OUTPUT_DIR} \
            -f ${fasta} -a 0 -t 2020-05-14 \
            |& tee "${LOG_DIR}/${protein_identity}.log"

            end=$(date +%s)
            runtime=$((end - start))

            echo "${protein_identity},${runtime}" >> $RUNTIME_CSV

       done <<< "$fastas"

    fi

done 