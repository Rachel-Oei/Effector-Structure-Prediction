#!/bin/bash

# Will run on GPU 0

# Move esm.pdb files to clustering folder 
ESM_DIR="/home/rachel/07_fold_all/effector_p/esm/esmfold-results"
ESM_PDB="/home/rachel/08_cluster_all/effector_p/esm/pdb"
ESM_TMP="/linuxhome/tmp/${USER}/effector_p/esm/"
FDSK_OUT="/home/rachel/08_cluster_all/effector_p/esm/foldseek_output"

mkdir -p ${ESM_PDB}
mkdir -p ${ESM_TMP}
mkdir -p ${FDSK_OUT}

for folder in "$ESM_DIR"/*; do

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

    echo "Moved $(basename "$pdb_file") → ${id}.pdb"

done

# Run foldseek easy-cluster on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-cluster ${ESM_PDB} "${FDSK_OUT}/esm_clusters" ${ESM_TMP}

# Run foldseek easy-search on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-search \
    ${ESM_PDB} \
    ${ESM_PDB} \
    ${FDSK_OUT}/esm_foldseek_results.tsv \
    ${ESM_TMP} \
    --format-output "query,target,alnlen,alntmscore,qtmscore,ttmscore,rmsd"
