# Activate .venv environment and pip install gemmi:
# python3 -m venv venv
# source venv/bin/activate
# pip install gemmi

import gemmi
import os

input_directory = "/home/rachel/cif/cif_downloads/"
output_directory = "/home/rachel/cif/cif_single_chain/"

os.makedirs(output_directory, exist_ok=True)

# Read PDB + chain list
with open("/home/rachel/cif/PDB_ID_list.txt") as f:
    protein_list = [line.strip() for line in f if line.strip()]

with open("/home/rachel/cif/PDB_ID_list2.txt") as f:
    protein_list_identity = [line.strip() for line in f if line.strip()]

for protein_id, protein_identity in zip(protein_list, protein_list_identity):
    pdb = protein_id[:4]
    chain_id = protein_id[5]

    cif_file = f"{input_directory}{pdb}.cif"

    # Read mmCIF
    structure = gemmi.read_structure(cif_file)

    # Keep only the requested chain
    found_chain = False

    for model in structure:
        chains_to_remove = []

        for chain in model:
            print("name:", chain.name)
            print("id:", chain_id)

            if chain.name != chain_id:
                chains_to_remove.append(chain.name)
            else:
                found_chain = True

        for chain_name in chains_to_remove:
            model.remove_chain(chain_name)

    if not found_chain:
        print(f"WARNING: Chain {chain_id} not found in {pdb}")
        continue

    # Write single-chain mmCIF
    output_file = f"{output_directory}{protein_identity}.cif"

    structure.make_mmcif_document().write_file(output_file)

    print(f"Created {output_file}")