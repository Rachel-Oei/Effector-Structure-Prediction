import json
import sys

sys.path.append("/home/rachel/01_prepare_cif")

from prepare_cif_models import pdb_text_to_list

def create_json (input_text_entity, input_text_chain, fasta_dir, output_dir):

    list_chain = pdb_text_to_list(input_text_chain)
    list_entity = pdb_text_to_list(input_text_entity)

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
            "name":f"{protein}_{entity}",
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
        
        output_file = f"{output_dir}/{protein}_{entity}.json"

        # Write the json file 
        with open(output_file, "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"{protein}_{entity}.json created")