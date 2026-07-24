import requests 
import os
import gemmi
from typing import List
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

def create_directory (nested_directory: str):
    """
    Creates directory
    """
    os.makedirs(nested_directory, exist_ok=True)

def pdb_text_to_list (input_text: str) -> List[str] : 
    """
    Converts PDB codes from a .txt separated by new-lines into a list
    Input: .txt file delimited by new-lines.
        Example: 
        1FN8.A
        1KG1.A
        1KPT.A
        4GVB.B
    Return: [1FN8.A, 1KG1.A, 1KPT.A, 4GVB.B]
    """
    lines = []
    with open(input_text, "r") as f:
        for line in f:
            lines.append(line[:6])
    return lines
    
def download_cif (input_text, output_directory):
    """
    Downloads cif files from RCSB, from PDB codes in the input list
    Output file name e.g: 1FN8.cif
    """
    input_lines = pdb_text_to_list(input_text)

    for protein_full in input_lines:
        protein_id=protein_full[:4]
        url = f"https://files.rcsb.org/download/{protein_id}.cif"
        output_final_directory=output_directory+f"{protein_id}.cif"
        response = requests.get(url, timeout=30)

        with open(output_final_directory, "wb") as out_file:
            out_file.write(response.content)

        print(f"Downloaded {protein_id}")

def map_chain_to_entity (input_text: str, cif_directory, new_text_directory):
    """
    Maps all pdb chains to entity number and stores it into a 
    similar format text file. 
    Input: .txt file delimited by new-lines.
        Example: 
        1FN8.A
        1KG1.A
        1KPT.A
        4GVB.B
    Return: .txt file delimited by new-lines.
        Example: 
        1FN8_1
        1KG1_1
        1KPT_1
        4GVB_1
    """
    input_list=pdb_text_to_list(input_text)

    input_list_entity=[]
    for protein_full in input_list:
        protein_id=protein_full[:4]
        protein_directory=f"{cif_directory}{protein_id}.cif"
        d = MMCIF2Dict(protein_directory)
        cif_entity_ids = d["_atom_site.label_entity_id"]
        cif_chains = d["_atom_site.auth_asym_id"]
        
        protein_chain=protein_full[5]
        entity_id=None
        for cif_entity_id, cif_chain in zip(cif_entity_ids, cif_chains):
            if protein_chain == cif_chain:
                entity_id=cif_entity_id
                break

        if entity_id is None:
            print(f"Could not find chain {protein_full}")
            continue

        input_list_entity.append(f"{protein_id}_{entity_id}")

    with open(new_text_directory, "w") as text_file:
        for protein_with_entity in input_list_entity:
            text_file.write(protein_with_entity+"\n")

def extract_chain_sequences(input_text, cif_directory, cif_fasta_directory):
    """
    Obtain fasta sequences from only the single chains that are used.
    """
    input_list=pdb_text_to_list(input_text)
    for protein_full in input_list:
        protein_id=protein_full[:4]
        entity_id=protein_full[5]
        protein_directory=f"{cif_directory}{protein_id}.cif"
        d = MMCIF2Dict(protein_directory)
        strand_ids = d["_entity_poly.entity_id"]
        sequences = d["_entity_poly.pdbx_seq_one_letter_code_can"]

        chain_sequence=None
        for strand_id, sequence in zip(strand_ids, sequences):
            if entity_id == strand_id:
                chain_sequence=sequence.replace("\n", "")
                break

        if chain_sequence is None:
            print(f"Could not find sequence {protein_full}")
            continue 

        output_file = f"{cif_fasta_directory}{protein_full}.fasta"

        with open(output_file, "w") as f:
            f.write(f">{protein_full}\n")
            f.write(chain_sequence + "\n")

        print(f"Created {output_file}")

def cif_single_chain (input_text_chain, 
                      input_text_entity, 
                      cif_download_directory, 
                      cif_single_chain_directory
                      ):
    chain_list = pdb_text_to_list(input_text_chain)
    entity_list = pdb_text_to_list(input_text_entity)

    for id_with_chain, id_with_entity in zip (chain_list, entity_list):
        full_protein_id=id_with_entity[:6]
        protein_id=id_with_chain[:4]
        protein_chain=id_with_chain[5]

        cif_file=f"{cif_download_directory}{protein_id}.cif"
        structure = gemmi.read_structure(cif_file)

        found_chain = False
        for model in structure:
            chains_to_remove=[]
    
            for chain in model:
                print("name:", chain.name)
                print("id:", protein_chain)
    
                if chain.name != protein_chain:
                    chains_to_remove.append(chain.name)
                else:
                    found_chain = True
    
            for chain_name in chains_to_remove:
                model.remove_chain(chain_name)
    
        if not found_chain:
            print(f"WARNING: Chain {protein_chain} not found in {protein_id}")
            continue
    
        # Write single-chain mmCIF
        output_file = f"{cif_single_chain_directory}{full_protein_id}.cif"

        structure.make_mmcif_document().write_file(output_file)
    
        print(f"Created {output_file}")
