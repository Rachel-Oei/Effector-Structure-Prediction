from prepare_cif_models import (create_directory, 
                                download_cif, 
                                map_chain_to_entity, 
                                extract_chain_sequences, 
                                cif_single_chain
)

def main():
    home_directory = "/home/rachel"

    input_text_chain = home_directory + "/01_prepare_cif/input_pdb_lists/pdb_list_chain.txt"
    input_text_entity = home_directory + "/01_prepare_cif/input_pdb_lists/pdb_list_entity.txt"

    cif_fasta_directory = home_directory + "/01_prepare_cif/cif_fasta/"
    cif_download_directory = home_directory + "/01_prepare_cif/cif_downloads/"
    cif_single_chain_directory = home_directory + "/01_prepare_cif/cif_single_chain/"

    create_directory(cif_download_directory)
    create_directory(cif_fasta_directory)
    create_directory(cif_single_chain_directory)

    download_cif(input_text_chain, cif_download_directory)
    map_chain_to_entity(input_text_chain, cif_download_directory, input_text_entity)
    extract_chain_sequences(input_text_entity, cif_download_directory, cif_fasta_directory)
    cif_single_chain(
        input_text_chain, 
        input_text_entity, 
        cif_download_directory, 
        cif_single_chain_directory
        )

if __name__ == "__main__":
    main()