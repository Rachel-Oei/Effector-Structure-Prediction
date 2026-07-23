import requests 
import os
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

def write_file (response, output_final_directory):
    """
    Writes files to directory
    """
    with open(output_final_directory, "wb") as out_file:
        out_file.write(response.content)
    
def download_cif (input_lines, output_directory):
    """
    Downloads cif files from RCSB, from PDB codes in the input list
    Output file name e.g: 1FN8.cif
    """
    for protein_full in input_lines:
        protein_id=protein_full[:4]
        url = f"https://files.rcsb.org/download/{protein_id}.cif"
        output_final_directory=output_directory+f"{protein_id}.cif"
        response = requests.get(url, timeout=30)
        write_file(response, output_final_directory)
        print(f"Downloaded {protein_id}")

def map_chain_to_entity (input_text: str, output_directory) -> str:
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

    for protein in input_list:
        


# def get_sequence_by_chain(cif_file, chain):
#     d = MMCIF2Dict(cif_file)

#     strand_ids = d["_entity_poly.entity_id"]
#     print(strand_ids)
#     sequences = d["_entity_poly.pdbx_seq_one_letter_code_can"]
#     print(sequences)

#     for strand_id, sequence in zip(strand_ids, sequences):
#         if chain in strand_id.split(","):
#             return sequence.replace("\n", "")

def main():
    home_directory = "/home/rachel"
    input_text = home_directory + "/cif/input_pdb_lists/pdb_list_chain.txt"
    output_directory = home_directory + "/cif/cif_downloads/"
    create_directory(output_directory)
    input_list = pdb_text_to_list(input_text)
    download_cif(input_list, output_directory)

if __name__ == "__main__":
    main()