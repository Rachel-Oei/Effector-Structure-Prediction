#!/bin/bash

# Need to create model parameters inside "/home/rachel/02_folding/af3/alphafold3-3.0.3/af3.bin.zst"
# Create other folder 
AF3_DIR="/home/rachel/02_folding/af3/run_alphafold.sh"
JSON_DIR="/home/rachel/02_folding/af3/json"
MODEL_DIR="/home/rachel/02_folding/af3/alphafold-models-3.0.3"
DB_DIR="/net/leca/linuxhome/alphafold/alphafold-db-3.0.3"
OUTPUT_DIR="/home/rachel/02_folding/af3/alphafold3-3.0.3/output"

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

    # Use specifically GPU 0 
    APPTAINERENV_CUDA_VISIBLE_DEVICES=0 ${AF3_DIR} \
      --json_path=${json_file} \
      --model_dir=${MODEL_DIR} \
      --db_dir=${DB_DIR} \
      --output_dir=${OUTPUT_DIR}

    echo "Finished ${json_file}"
done