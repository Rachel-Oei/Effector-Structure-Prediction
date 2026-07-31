#!/bin/bash

MULTI_FASTA_DIR="/home/rachel/07_fold_all/effector_p/multi_fasta"
SINGLE_FASTA_DIR="/home/rachel/07_fold_all/effector_p/single_fasta"

mkdir -p "$SINGLE_FASTA_DIR"

for multi_fasta in "$MULTI_FASTA_DIR"/*.fasta; do

    # Get filename without .fasta
    name=$(basename "$multi_fasta" __protein_sequences.fasta)

    awk -v output_dir="$SINGLE_FASTA_DIR" -v name="$name" '
    /^>/ {
        # Get first identifier after >
        protein_id = $2

        outfile = output_dir "/" name "_" protein_id ".fasta"
    }

    {print > outfile}

    ' "$multi_fasta"

done

echo "Finished splitting FASTA files."