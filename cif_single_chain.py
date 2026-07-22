# Activate .venv environment and pip install gemmi

import gemmi
import os

input_directory = "/home/rachel/cif/cif_downloads/"
output_directory = "/home/rachel/cif/cif_single_chain/"

os.makedirs(output_directory, exist_ok=True)

# Read PDB + chain list
with open("/home/rachel/cif/PDB_ID_list.txt") as f:
    protein_list = [line.strip() for line in f if line.strip()]

for protein_id in protein_list:

    pdb = protein_id[:4]
    chain_id = protein_id[5]   # label_asym_id, e.g. A

    cif_file = f"{input_directory}{pdb}.cif"

    # Read mmCIF
    structure = gemmi.read_structure(cif_file)

    # Keep only the requested chain
    found_chain = False

    for model in structure:
        for chain in list(model):
            if chain.name != chain_id:
                model.remove_chain(chain.name)
            else:
                found_chain = True

    if not found_chain:
        print(f"WARNING: Chain {chain_id} not found in {pdb}")
        continue

    # Write single-chain mmCIF
    output_file = f"{output_directory}{protein_id}.cif"

    structure.make_mmcif_document().write_file(output_file)

    print(f"Created {output_file}")