#!/bin/bash

JSON_DIR="/home/rachel/alphafold3-3.0.3"
MODEL_DIR="/home/rachel/alphafold-models-3.0.3"
DB_DIR="/net/leca/linuxhome/alphafold/alphafold-db-3.0.3"
OUTPUT_DIR="/home/rachel/alphafold3-3.0.3/output"

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

    # Use specifically GPU 0 
    APPTAINERENV_CUDA_VISIBLE_DEVICES=0 /home/jankees-alphafold-303/alphafold3-3.0.3/run_alphafold.sh \
      --json_path=${json_file} \
      --model_dir=${MODEL_DIR} \
      --db_dir=${DB_DIR} \
      --output_dir=${OUTPUT_DIR}

    echo "Finished ${json_file}"
done

