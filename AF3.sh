
# Put the file af3.bin.zst in ${HOME}/alphafold-models-3.0.3 and unpack it

mkdir -p /home/rachel/alphafold-models-3.0.3
scp "/Users/522112/Downloads/ECTRIE/Soft Matter Physics/Oxysporum/AF3/af3.bin.zst" \
 rachel@alive.bio.uu.nl:/home/rachel/alphafold-models-3.0.3

# Move into the folder 
cd /home/rachel/alphafold-models-3.0.3
# Unpack the model parameters from Google Deepmind
zst -d af3.bin.zst

#Create .json file (see how this is a different AF3 folder than the "models" folder)
touch /home/rachel/alphafold3-3.0.3/fold_input.json
nano /home/rachel/alphafold3-3.0.3/fold_input.json

#Create output directory in that folder 
mkdir -p /home/rachel/alphafold3-3.0.3/output

# Go in the binfgpu server 
bash /home/rachel/alphafold-models-3.0.3/run_all_AF3.sh










