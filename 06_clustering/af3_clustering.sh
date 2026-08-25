#!/bin/bash

# Will run on GPU 0

HOME_DIR="/home/rachel"
mkdir -p "${HOME_DIR}/06_clustering"
cd "${HOME_DIR}/06_clustering"

export PATH=$(pwd)/foldseek/bin/:$PATH

# Move af3.cif files to clustering folder 
AF3_DIR="/home/rachel/02_folding/af3/alphafold3-3.0.3/output"
AF3_CIF="/home/rachel/06_clustering/af3/cif"
AF3_TMP="/linuxhome/tmp/${USER}/alphafold3/"
FDSK_OUT="/home/rachel/06_clustering/af3/foldseek_output"

mkdir -p ${AF3_CIF}
mkdir -p ${AF3_TMP}
mkdir -p ${FDSK_OUT}

for folder in "$AF3_DIR"/*; do

    id=$(basename "$folder")
    predicted="$AF3_DIR/${id}/${id}_model.cif"

    cif_file="${AF3_CIF}/${id}_model.cif"
        
    if [ -f "$cif_file" ]; then
    echo "Skipping ${id}: already moved"
    continue
    fi

    cp ${predicted} ${AF3_CIF}/${id}_model.cif

    echo "Moved ${id}_model.cif to 06_clustering/af3/cif"

done 

# Run foldseek easy-cluster on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-cluster ${AF3_CIF} "${FDSK_OUT}/af3_clusters" ${AF3_TMP}

# Run foldseek easy-search on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-search \
    ${AF3_CIF} \
    ${AF3_CIF} \
    ${FDSK_OUT}/_af3_foldseek_results.tsv \
    ${AF3_TMP} \
    --format-output "query,target,alnlen,alntmscore,qtmscore,ttmscore,rmsd"

# Use tmscore normalized by alignment length: alntmscore