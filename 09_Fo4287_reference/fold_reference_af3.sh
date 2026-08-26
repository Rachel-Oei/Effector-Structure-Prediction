#!/bin/bash

# The script is executed with either "effector_p" or "foec_2" as the first option.
# Second option specifies the gpu, so "0" or "1".
# Example: bash fold_reference_esm.sh foec_2 1

PIPELINE="$1"
GPU="$2"

# Check whether pipeline is correct 
if [[ "$PIPELINE" != "effector_p" && "$PIPELINE" != "foec_2" ]]; then
    echo "Error: pipeline must be 'effector_p' or 'foec_2'"
    exit 1
fi

if [[ "$GPU" != "0" && "$GPU" != "1" ]]; then
    echo "Error: GPU must be '0' or '1'"
    exit 1
fi

AF3_FOLDER="/home/rachel/09_Fo4287_reference/${PIPELINE}/af3"
AF3_DIR="/home/rachel/02_folding/af3/run_alphafold.sh"
JSON_DIR="${AF3_FOLDER}/json"
MODEL_DIR="/home/rachel/02_folding/af3/alphafold-models-3.0.3"
DB_DIR="/net/leca/linuxhome/alphafold/alphafold-db-3.0.3"
OUTPUT_DIR="${AF3_FOLDER}/alphafold3-3.0.3/output"
RUNTIME_CSV="${AF3_FOLDER}/af3_runtime.csv"

mkdir -p ${OUTPUT_DIR}

for json_file in "${JSON_DIR}"/*.json
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

    # Use specifically 
    APPTAINERENV_CUDA_VISIBLE_DEVICES=${GPU} ${AF3_DIR} \
      --json_path=${json_file} \
      --model_dir=${MODEL_DIR} \
      --db_dir=${DB_DIR} \
      --output_dir=${OUTPUT_DIR}

    end=$(date +%s)
    runtime=$((end - start))
    
    echo "Finished ${json_file}"
    
    echo "${protein_identity},${runtime}" >> $RUNTIME_CSV

done