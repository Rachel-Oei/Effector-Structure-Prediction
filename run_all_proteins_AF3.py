# I want this code to create all .json files like:
# /home/rachel/alphafold3-3.0.3/1FN8.json
# /home/rachel/alphafold3-3.0.3/1KG1.json

import json

# Make the text file into a list
with open("/home/rachel/cif/PDB_ID_list2.txt") as f:
    protein_ID_list = [line.strip() for line in f if line.strip()]

for protein_id in protein_ID_list:
    protein=protein_id[:4]
    chain=protein_id[6]
    sequence="/home/rachel/cif/cif_fasta/{protein_id}.fasta"

    # Read the FASTA sequence
    fasta_file = f"/home/rachel/cif/cif_fasta/{protein_id}.fasta"

    # Open the FASTA file and only extract the sequence 
    with open(fasta_file) as f:
        sequence = "".join(
            line.strip()
            for line in f
            if not line.startswith(">")
        )

    json_data={
        "name": protein,
        "sequences": [
        {
            "protein": {
            "id": [chain],
            "sequence": sequence
            }
        }
        ],
        "modelSeeds": [1],
        "dialect": "alphafold3",
        "version": 1
    }
    
    output_file = f"/home/rachel/alphafold3-3.0.3/{protein}.json"

    # Write the json file 
    with open(output_file, "w") as f:
        json.dump(json_data, f, indent=2)

    nano /home/rachel/alphafold3-3.0.3/{protein}.json
    json_file
    
    print(f"{protein}.json created")


