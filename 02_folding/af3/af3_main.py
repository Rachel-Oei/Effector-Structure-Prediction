import sys

sys.path.append("/home/rachel/01_prepare_cif")

from prepare_cif_models import pdb_text_to_list, create_directory
from af3_models import create_json

def main():
    cif_directory = "/home/rachel/01_prepare_cif"
    input_text_chain = cif_directory+"/input_pdb_lists/pdb_list_chain.txt"
    input_text_entity = cif_directory+"/input_pdb_lists/pdb_list_entity.txt"
    fasta_dir=cif_directory+"/cif_fasta"

    list_chain = pdb_text_to_list(input_text_chain)
    list_entity = pdb_text_to_list(input_text_entity)

    output_dir="/home/rachel/02_folding/af3"
    create_directory (output_dir)

    create_json(list_entity, list_chain, fasta_dir, output_dir)

if __name__ == "__main__":
    main()