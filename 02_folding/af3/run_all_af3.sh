#!/bin/bash

# This script uses GPU 0. Runs AF3 for each protein and appends runtime in a .csv file. 

AF3_FOLDER="/home/rachel/02_folding/af3"

AF3_DIR="${AF3_FOLDER}/run_alphafold.sh"
JSON_DIR="${AF3_FOLDER}/json"
MODEL_DIR="${AF3_FOLDER}/alphafold-models-3.0.3"
DB_DIR="/net/leca/linuxhome/alphafold/alphafold-db-3.0.3"
OUTPUT_DIR="${AF3_FOLDER}/alphafold3-3.0.3/output"
RUNTIME_CSV="${AF3_FOLDER}/af3_runtime.csv"

mkdir -p ${MODEL_DIR}

for json_file in ${JSON_DIR}/*.json
do
    protein_identity=$(basename "$json_file" .json)

    summary_file="${OUTPUT_DIR}/${protein_identity}/${protein_identity}_summary_confidences.json"

    # Skip if AF3 output already exists
    if [ -f "$summary_file" ]; then
        echo "Skipping ${protein_identity}: already completed"
        continue
    fi

    echo "Starting AF3 for ${json_file}"

    # Collect runtime 
    start=$(date +%s)

    # Use specifically GPU 0 
    APPTAINERENV_CUDA_VISIBLE_DEVICES=0 ${AF3_DIR} \
      --json_path=${json_file} \
      --model_dir=${MODEL_DIR} \
      --db_dir=${DB_DIR} \
      --output_dir=${OUTPUT_DIR}

    end=$(date +%s)
    runtime=$((end - start))
    
    echo "Finished ${json_file}"
    
    echo "${protein_identity},${runtime}" >> $RUNTIME_CSV

done