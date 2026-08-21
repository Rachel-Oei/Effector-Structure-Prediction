from prepare_cif_models import Protein, AllProteins
import os

def main():
    cif_directory = "/home/rachel/01_prepare_cif"
    input_text_chain = cif_directory + "/input_pdb_lists/pdb_list_chain.txt"

    cif_download_directory = cif_directory + "/cif_downloads/"
    os.makedirs(cif_download_directory, exist_ok=True)

    cif_fasta_directory = cif_directory + "/cif_fasta/"
    os.makedirs(cif_fasta_directory, exist_ok=True)

    cif_single_chain_directory = cif_directory + "/cif_single_chain/"
    os.makedirs(cif_single_chain_directory, exist_ok=True)

    proteins = AllProteins(input_text_chain)
    proteins.download_all(cif_download_directory)
    proteins.map_entities(cif_download_directory)
    proteins.extract_chain_sequences(cif_download_directory, cif_fasta_directory)
    proteins.cif_single_chain_all(cif_download_directory, cif_single_chain_directory)

if __name__ == "__main__":
    main()