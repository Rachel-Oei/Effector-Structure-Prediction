#!/bin/bash

begins=`date +%s`

if [ $# == 0 ] ; then
  echo "Run predictions example:
  
$0 \\
  --json_path=/home/rachel/02_folding/af3/json/fold_input.json \\
  --model_dir=/home/rachel/02_folding/af3/alphafold-models-3.0.3 \\
  --db_dir=/net/leca/linuxhome/alphafold/alphafold-db-3.0.3 \\
  --output_dir=/home/rachel/02_folding/af3/alphafold3-3.0.3/output

Or for specific GPU (e.g GPU1):

APPTAINERENV_CUDA_VISIBLE_DEVICES=1 \\
  $0 \\
  --json_path=/home/rachel/02_folding/af3/alphafold3-3.0.3/json/fold_input.json \\
  --model_dir=/home/rachel/02_folding/af3/alphafold-models-3.0.3 \\
  --db_dir=/net/leca/linuxhome/alphafold/alphafold-db-3.0.3 \\
  --output_dir=/home/rachel/02_folding/af3/alphafold3-3.0.3/output
  
Or 

$0 --help

Or

$0 --helpfull
(Takes some time...)
"
  exit
fi
  

## jankees-alphafold-303
export ALPHAUSER=/home/jankees-alphafold-303

unset PYTHONPATH
unset PYTHONHOME

export PYTHONNOUSERSITE=1

export PATH=${ALPHAUSER}/miniforge3/envs/alphafold-3.0.3/bin:$PATH
export LD_LIBRARY_PATH=${ALPHAUSER}/miniforge3/envs/alphafold-3.0.3/lib

if [ -z ${APPTAINERENV_CUDA_VISIBLE_DEVICES} ] ; then
  export APPTAINERENV_CUDA_VISIBLE_DEVICES=0
fi

cd ${ALPHAUSER}/alphafold3-3.0.3

# Change the tmp to avoid overloading the /tmp
export AF3TMP=/linuxhome/tmp/${USER}/alphafold3/tmp
mkdir -vp ${AF3TMP}
export TMPDIR=${AF3TMP}
export APPTAINERENV_TMPDIR=${AF3TMP}
export SINGULARITY_TMPDIR=${AF3TMP}
export APPTAINER_TMPDIR=${AF3TMP}

# Set some caching dir:
export AF3CACHE=/linuxhome/tmp/${USER}/alphafold3/cache
mkdir -vp ${AF3CACHE}
export APPTAINER_CACHEDIR=${AF3CACHE}
export SINGULARITY_CACHEDIR=${AF3CACHE}

apptainer exec \
--nv \
--bind=/net:/net \
--bind=/linuxhome:/linuxhome \
./alphafold3.sif \
python run_alphafold.py "$@"

echo "
"
ends=`date +%s`
timesec=$((${ends}-${begins}))
#timemin=`echo ${timesec} | awk '{printf("%.2f\n",$1 / 60)}'`
timehrs=`echo ${timesec} | awk '{printf("%.2f\n",$1 / 3600)}'`
echo "Total time of `basename $0` was: ${timesec} sec (or approx. ${timehrs} hours)"