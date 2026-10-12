#!/bin/bash

# The script is executed with either "effector_p" or "foec_2" as the first option.
# Second option specifies the gpu, so "0" or "1".
# Example: bash cluster_reference_af3.sh foec_2 1

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

# All _model.cif files are inside separate folders. 
# We want to copy them out and put them into one clustering folder.
AF3_DIR="/home/rachel/09_Fo4287_reference/${PIPELINE}/af3/alphafold3-3.0.3/output"
AF3_CIF="/home/rachel/10_cluster_reference/${PIPELINE}/af3/cif"

# Create tmp folder
AF3_TMP="/linuxhome/tmp/${USER}/cluster/${PIPELINE}/af3/"

FDSK_OUT="/home/rachel/10_cluster_reference/${PIPELINE}/af3/foldseek_output"

mkdir -p ${AF3_CIF}
mkdir -p ${AF3_TMP}
mkdir -p ${FDSK_OUT}

for folder in "$AF3_DIR"/*; do

    # Take the name of the folder for the new .cif name
    id=$(basename "$folder")
    predicted=("$folder"/*.cif)

    if [ ! -f "${predicted[0]}" ]; then
        echo "Warning: no cif found for ${id}"
        continue
    fi

    pdb_file="${predicted[0]}"
    destination="$AF3_CIF/${id}.cif"

    # Check whether this folder has already been copied
    if [ -f "$destination" ]; then
        echo "Skipping ${id}: already moved"
        continue
    fi

    cp "$pdb_file" "$destination"

    echo "Copied $(basename "$pdb_file") → ${id}.cif"

done

# Run foldseek easy-cluster.
CUDA_VISIBLE_DEVICES=$GPU foldseek easy-cluster ${AF3_CIF} "${FDSK_OUT}/af3_clusters" ${AF3_TMP}

# Run foldseek easy-search.
CUDA_VISIBLE_DEVICES=$GPU foldseek easy-search \
    ${AF3_CIF} \
    ${AF3_CIF} \
    ${FDSK_OUT}/af3_foldseek_results.tsv \
    ${AF3_TMP} \
    --format-output "query,target,alnlen,alntmscore,qtmscore,ttmscore,rmsd"
