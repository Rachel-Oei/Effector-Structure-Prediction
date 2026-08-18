from prepare_cif_models import (prepare_cif)

def main():

    cif_directory = "/home/rachel/01_prepare_cif"
    
    prepare_cif (
        input_list = cif_directory + "/input_pdb_lists/pdb_list_chain.txt",
        download_dir = cif_directory + "/cif_downloads/",
        output_dir = cif_directory + "/cif_single_chain/"
    )

if __name__ == "__main__":
    main()