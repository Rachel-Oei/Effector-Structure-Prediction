#!/bin/bash

# The script is executed with either "effector_p" or "foec_2" as the first option.
# Second option specifies the gpu, so "0" or "1".
# Example: bash cluster_all_esm.sh foec_2 1

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

# All esm.pdb files are inside separate folders. 
# We want to copy them out and put them into one clustering folder.
ESM_DIR="/home/rachel/07_fold_all/${PIPELINE}/esm/esmfold-results"
ESM_PDB="/home/rachel/08_cluster_all/${PIPELINE}/esm/pdb"

# Create tmp folder
ESM_TMP="/linuxhome/tmp/${USER}/cluster/${PIPELINE}/esm/"

FDSK_OUT="/home/rachel/08_cluster_all/${PIPELINE}/esm/foldseek_output"

mkdir -p ${ESM_PDB}
mkdir -p ${ESM_TMP}
mkdir -p ${FDSK_OUT}

for folder in "$ESM_DIR"/*; do

    # Take the name of the folder for the new .pdb name
    id=$(basename "$folder")
    predicted=("$folder"/*.pdb)

    if [ ! -f "${predicted[0]}" ]; then
        echo "Warning: no PDB found for ${id}"
        continue
    fi

    pdb_file="${predicted[0]}"
    destination="$ESM_PDB/${id}.pdb"

    # Check whether this folder has already been copied
    if [ -f "$destination" ]; then
        echo "Skipping ${id}: already moved"
        continue
    fi

    cp "$pdb_file" "$destination"

    echo "Copied $(basename "$pdb_file") → ${id}.pdb"

done

# Run foldseek easy-cluster.
CUDA_VISIBLE_DEVICES=$GPU foldseek easy-cluster ${ESM_PDB} "${FDSK_OUT}/esm_clusters" ${ESM_TMP}

# Run foldseek easy-search.
CUDA_VISIBLE_DEVICES=$GPU foldseek easy-search \
    ${ESM_PDB} \
    ${ESM_PDB} \
    ${FDSK_OUT}/esm_foldseek_results.tsv \
    ${ESM_TMP} \
    --format-output "query,target,alnlen,alntmscore,qtmscore,ttmscore,rmsd"
