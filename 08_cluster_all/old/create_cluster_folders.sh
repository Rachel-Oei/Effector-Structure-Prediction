#!/bin/bash

# Creates the cluster folders, skip if already created.
for file in /home/rachel/*07_fold_all*/old/old_foec_2/p_effector_*.afa; do
    name=$(basename "$file" .afa)

    if [ -d "/home/rachel/07_fold_all/foec_2/clusters/${name}" ]; then
        echo "Skipping ${name}: folder already created"
        continue
    fi
    mkdir -p "/home/rachel/07_fold_all/foec_2/clusters/$name"
done

    
for fasta in /07_fold_all/old/foec_2/single_cut_fasta; do



    name=$(basename "$file" .afa)
