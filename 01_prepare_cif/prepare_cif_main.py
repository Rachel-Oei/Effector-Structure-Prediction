from prepare_cif_models import (create_directory, 
                                download_cif, 
                                map_chain_to_entity, 
                                extract_chain_sequences, 
                                cif_single_chain
)

# Make sure that the following file and directory exists: "/01_prepare_cif/input_pdb_lists/pdb_list_chain.txt"

def main():
    cif_directory = "/home/rachel/01_prepare_cif"

    input_text_chain = cif_directory + "/input_pdb_lists/pdb_list_chain.txt"
    input_text_entity = cif_directory + "/input_pdb_lists/pdb_list_entity.txt"

    cif_fasta_directory = cif_directory + "/cif_fasta/"
    cif_download_directory = cif_directory + "/cif_downloads/"
    cif_single_chain_directory = cif_directory + "/cif_single_chain/"

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