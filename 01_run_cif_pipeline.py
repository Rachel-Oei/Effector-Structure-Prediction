import requests 

def PDB_text_to_list (input_text: str) -> List : 
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

    return (lines)

    
def download_cif (input_lines, output_directory)
    """

    """
    # Stores the PDB ID's with only the first 4 characters inside a list
    lines = []
    with open(input_file, "r") as f:
        for line in f:
            lines.append(line[:4])

    # Downloads the .cif file for each protein id.
    for protein_id in lines:
        url = f"https://files.rcsb.org/download/{protein_id}.cif"
        output_final_directory=output_directory+f"{protein_id}.cif"

        response = requests.get(url, timeout=30)
        with open(output_final_directory, "wb") as out_file:
                out_file.write(response.content)
        print(f"Downloaded {protein_id}")

        return


#Set the directories
home_directory="/home/rachel"
input_lists=home_directory+"/cif/input_PDB_lists/PDB_ID_list.txt"
output_directory=home_directory+"/cif/cif_downloads/"

#Run the functions
input_list=PDB_text_to_list(input_text)
download_cif(input_list, output_directory)
