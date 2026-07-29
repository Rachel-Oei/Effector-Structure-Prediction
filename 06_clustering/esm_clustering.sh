# Will run on GPU 0

HOME_DIR="/home/rachel"
mkdir -p "${HOME_DIR}/06_clustering"
cd "${HOME_DIR}/06_clustering"

# Download Foldseek through:
# wget https://mmseqs.com/foldseek/foldseek-linux-gpu.tar.gz
# tar xvzf foldseek-linux-gpu.tar.gz

export PATH=$(pwd)/foldseek/bin/:$PATH

# Move esm.pdb files to clustering folder 
ESM_DIR="/home/rachel/02_folding/esm/esmfold-results"
ESM_PDB="/home/rachel/06_clustering/esm/pdb"
ESM_TMP="/linuxhome/tmp/${USER}/esm/"
FDSK_OUT="/home/rachel/06_clustering/esm/foldseek_output"

mkdir -p ${ESM_PDB}
mkdir -p ${ESM_TMP}
mkdir -p ${FDSK_OUT}

for folder in "$ESM_DIR"/*; do

    id=$(basename "$folder")
    predicted="$ESM_DIR/${id}/${id}.pdb"

    pdb_file="${ESM_PDB}/${id}.pdb"
        
    if [ -f "$pdb_file" ]; then
    echo "Skipping ${id}: already moved"
    continue
    fi

    cp ${predicted} ${ESM_PDB}/${id}.pdb

    echo "Moved ${id}.pdb to 06_clustering/esm/pdb"

done 

# Run foldseek easy-cluster on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-cluster ${ESM_PDB} "${FDSK_OUT}/esm_clusters" ${ESM_TMP}

# Run foldseek easy-search on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-search \
    ${ESM_PDB} \
    ${ESM_PDB} \
    ${FDSK_OUT}/esm_foldseek_results.tsv \
    ${ESM_TMP} \
    --format-output "query,target,alnlen,alntmscore,rmsd"

# Use tmscore normalized by alignment length: alntmscore