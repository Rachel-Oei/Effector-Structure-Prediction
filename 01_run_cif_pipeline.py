import requests 
from typing import List

def pdb_text_to_list (input_text: str) -> List[str] : 
    """Converts PDB codes from a .txt separated by new-lines into a list
        Input: .txt file with whitespaces.
                example: 
                1FN8.A
                1KG1.A
                1KPT.A
                4GVB.B
        Return: [1FN8, 1KG1, 1KPT, 4GVB]
    """
    lines = []
    with open(input_text, "r") as f:
        for line in f:
            lines.append(line[:4])
    return lines

def write_file (response, output_final_directory):
    """Writes files to directory
    """
    with open(output_final_directory, "wb") as out_file:
        out_file.write(response.content)
    
def download_cif (input_lines, output_directory):
    """
    Downloads cif files from RCSB, from PDB codes in the input list
    """
    for protein_id in input_lines:
        url = f"https://files.rcsb.org/download/{protein_id}.cif"
        output_final_directory=output_directory+f"{protein_id}.cif"
        response = requests.get(url, timeout=30)
        write_file(response, output_final_directory)
        print(f"Downloaded {protein_id}")

def main():
    home_directory = "/home/rachel"
    input_text = home_directory + "/cif/input_pdb_lists/pdb_list_chain.txt"
    output_directory = home_directory + "/cif/cif_downloads/"
    input_list = pdb_text_to_list(input_text)
    download_cif(input_list, output_directory)

if __name__ == "__main__":
    main()

