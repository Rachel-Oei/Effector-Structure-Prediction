#!/bin/bash

# The script is executed with either "effector_p" or "foec_2" as the first option.
# Second option specifies the gpu, so "0" or "1".
# Example: bash cluster_all_af2.sh foec_2 1

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

# All ranked_0.pdb files are inside separate folders. 
# We want to copy them out and put them into one clustering folder.
AF2_DIR="/home/rachel/07_fold_all/${PIPELINE}/af2/alphafold-2.3.2/output/results"
AF2_PDB="/home/rachel/08_cluster_all/${PIPELINE}/af2/pdb"

# Create tmp folder
AF2_TMP="/linuxhome/tmp/${USER}/cluster/${PIPELINE}/af2/"

FDSK_OUT="/home/rachel/08_cluster_all/${PIPELINE}/af2/foldseek_output"

mkdir -p ${AF2_PDB}
mkdir -p ${AF2_TMP}
mkdir -p ${FDSK_OUT}

for folder in "$AF2_DIR"/*; do

    # Take the name of the folder for the new .pdb name
    id=$(basename "$folder")
    predicted=("$folder"/*.pdb)

    if [ ! -f "${predicted[0]}" ]; then
        echo "Warning: no PDB found for ${id}"
        continue
    fi

    pdb_file="${predicted[0]}"
    destination="$AF2_PDB/${id}.pdb"

    # Check whether this folder has already been copied
    if [ -f "$destination" ]; then
        echo "Skipping ${id}: already moved"
        continue
    fi

    cp "$pdb_file" "$destination"

    echo "Copied $(basename "$pdb_file") → ${id}.pdb"

done

# Run foldseek easy-cluster.
CUDA_VISIBLE_DEVICES=$GPU foldseek easy-cluster ${AF2_PDB} "${FDSK_OUT}/af2_clusters" ${AF2_TMP}

# Run foldseek easy-search.
CUDA_VISIBLE_DEVICES=$GPU foldseek easy-search \
    ${AF2_PDB} \
    ${AF2_PDB} \
    ${FDSK_OUT}/af2_foldseek_results.tsv \
    ${AF2_TMP} \
    --format-output "query,target,alnlen,alntmscore,qtmscore,ttmscore,rmsd"
