import sys
import subprocess 

sys.path.append("/home/rachel/01_prepare_cif")

from prepare_cif_models import create_directory
from create_json import create_json

def main():
    cif_directory = "/home/rachel/01_prepare_cif"
    input_text_entity = cif_directory+"/input_pdb_lists/pdb_list_entity.txt"
    input_text_chain = cif_directory+"/input_pdb_lists/pdb_list_chain.txt"
    fasta_dir=cif_directory+"/cif_fasta"
    json_output_dir="/home/rachel/02_folding/af3/json"
    af3_script="/home/rachel/02_folding/af3/run_all_af3.sh"

    create_directory(json_output_dir)
    create_json(input_text_entity, input_text_chain, fasta_dir, json_output_dir)

    subprocess.run(["bash", af3_script], check=True)

if __name__ == "__main__":
    main()