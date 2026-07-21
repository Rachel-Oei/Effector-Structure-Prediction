
# Put the file af3.bin.zst in ${HOME}/alphafold-models-3.0.3 and unpack it

mkdir -p home/rachel/alphafold-models-3.0.3
scp "/Users/522112/Downloads/ECTRIE/Soft Matter Physics/Oxysporum/AF3/af3.bin.zst" \
 rachel@alive.bio.uu.nl:/home/rachel/alphafold-models-3.0.3

# Move into the folder 
cd home/rachel/alphafold-models-3.0.3
# Unpack the model parameters from Google Deepmind
zst -d af3.bin.zst

#Create .json file:
touch home/rachel/alphafold3-3.0.3/fold_input.json
nano home/rachel/alphafold3-3.0.3/fold_input.json










