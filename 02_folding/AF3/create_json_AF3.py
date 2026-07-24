import json
import sys

cif_directory = "/home/rachel/01_prepare_cif"

sys.path.append(cif_directory)

from prepare_cif_models import pdb_text_to_list

input_text_chain = cif_directory+"/input_pdb_lists/pdb_list_chain.txt"
input_text_entity = cif_directory+"/input_pdb_lists/pdb_list_entity.txt"
fasta_dir=cif_directory+"/cif_fasta"

list_chain = pdb_text_to_list(input_text_chain)
list_entity = pdb_text_to_list(input_text_entity)

output_file

for entity, chain in zip(list_entity, list_chain):
    protein=entity[:4] #just 1FN8
    entity=entity[5]
    chain=chain[5]

    fasta_file = f"{fasta_dir}/{protein}_{entity}.fasta"

    with open(fasta_file) as f:
        sequence_lines = []
        for line in f:
            if not line.startswith(">"):
                sequence_lines.append(line.strip())
        sequence = "".join(sequence_lines)

    json_data={
        "name":f"{protein}_{entity}"
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
    
    output_file = f"/home/rachel/alphafold3-3.0.3/{protein}_{entity}.json"

    # Write the json file 
    with open(output_file, "w") as f:
        json.dump(json_data, f, indent=2)

    print(f"{protein}_{entity}.json created")


