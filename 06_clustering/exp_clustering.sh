# Will run on GPU 0

HOME_DIR="/home/rachel"
mkdir -p "${HOME_DIR}/06_clustering"
cd "${HOME_DIR}/06_clustering"

# Download Foldseek through:
# wget https://mmseqs.com/foldseek/foldseek-linux-gpu.tar.gz
# tar xvzf foldseek-linux-gpu.tar.gz

export PATH=$(pwd)/foldseek/bin/:$PATH

# Move af3.cif files to clustering folder 
EXP_CIF="/home/rachel/01_prepare_cif/cif_single_chain"
EXP_TMP="/linuxhome/tmp/${USER}/experimental_structures/"
FDSK_OUT="/home/rachel/06_clustering/experimental/foldseek_output"

mkdir -p ${EXP_TMP}
mkdir -p ${FDSK_OUT}

#Run foldseek on GPU 0
CUDA_VISIBLE_DEVICES=0 foldseek easy-cluster ${EXP_CIF} "${FDSK_OUT}/experimental_clusters" ${EXP_TMP}

# Run foldseek easy-search on GPU 0 
CUDA_VISIBLE_DEVICES=0 foldseek easy-search \
    ${EXP_CIF} \
    ${EXP_CIF} \
    ${FDSK_OUT}/exp_foldseek_results.tsv \
    ${EXP_TMP} \
    --format-output "query,target,alnlen,alntmscore,rmsd"

# Use tmscore normalized by alignment length: alntmscore