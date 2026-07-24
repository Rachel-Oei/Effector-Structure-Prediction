import json

home_directory = "/home/rachel"
input_text_chain = home_directory + "/01_prepare_cif/input_pdb_lists/pdb_list_chain.txt"
input_text_entity = home_directory + "/01_prepare_cif/input_pdb_lists/pdb_list_entity.txt"


# Make the text file into a list
with open("/home/rachel/cif/PDB_ID_list2.txt") as f:
    protein_ID_list_identities = [line.strip() for line in f if line.strip()]

with open("/home/rachel/cif/PDB_ID_list.txt") as f:
    protein_ID_list_chains = [line.strip() for line in f if line.strip()]

for identity, chain in zip(protein_ID_list_identities, protein_ID_list_chains):
    protein=identity[:4]
    identity=identity[5]
    chain=chain[5]

    # Read the FASTA sequence
    fasta_file = f"/home/rachel/cif/cif_fasta/{protein}_{identity}.fasta"

    # Open the FASTA file and only extract the sequence 
    with open(fasta_file) as f:
        sequence = "".join(
            line.strip()
            for line in f
            if not line.startswith(">")
        )

    json_data={
        "name":f"{protein}_{identity}"
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
    
    output_file = f"/home/rachel/alphafold3-3.0.3/{protein}_{identity}.json"

    # Write the json file 
    with open(output_file, "w") as f:
        json.dump(json_data, f, indent=2)

    print(f"{protein}_{identity}.json created")


