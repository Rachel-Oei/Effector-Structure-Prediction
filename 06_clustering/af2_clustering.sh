#!/bin/bash

# Will run on GPU 0

HOME_DIR="/home/rachel"
mkdir -p "${HOME_DIR}/06_clustering"
cd "${HOME_DIR}/06_clustering"

export PATH=$(pwd)/foldseek/bin/:$PATH

# Move af2.cif files to clustering folder 
AF2_DIR="/home/rachel/02_folding/af2/alphafold-2.3.2/output/results"
AF2_PDB="/home/rachel/06_clustering/af2/pdb"
AF2_TMP="/linuxhome/tmp/${USER}/alphafold2/"
FDSK_OUT="/home/rachel/06_clustering/af2/foldseek_output"

mkdir -p ${AF2_PDB}
mkdir -p ${AF2_TMP}
mkdir -p ${FDSK_OUT}

for folder in "$AF2_DIR"/*; do

    id=$(basename "$folder")
    predicted="$AF2_DIR/${id}/ranked_0.pdb"

    pdb_file="${AF2_PDB}/${id}.pdb"
        
    if [ -f "$pdb_file" ]; then
    echo "Skipping ${id}: already moved"
    continue
    fi

    cp ${predicted} ${AF2_PDB}/${id}.pdb

    echo "Moved ${id}/ranked_0.pdb to 06_clustering/af2/pdb"

done 

# Run foldseek easy-cluster on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-cluster ${AF2_PDB} "${FDSK_OUT}/af2_clusters" ${AF2_TMP}

# Run foldseek easy-search on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-search \
    ${AF2_PDB} \
    ${AF2_PDB} \
    ${FDSK_OUT}/af2_foldseek_results.tsv \
    ${AF2_TMP} \
    --format-output "query,target,alnlen,alntmscore,qtmscore,ttmscore,rmsd"

# Use tmscore normalized by alignment length: alntmscore