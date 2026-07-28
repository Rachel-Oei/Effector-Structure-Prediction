from results_to_tsv import results_to_tsv

def main():
    home_dir="/home/rachel"
    tmalign_folder = home_dir+"/03_tm_align"
    output_dir = home_dir+"/04_results_tsv"

    model1="esm"
    metadata_file_esm = output_dir+"/pdb_metadata_with_dates.tsv"
    runtime_file_esm=home_dir+"/02_folding/esm/esm_runtime.csv"
    results_to_tsv(tmalign_folder, output_dir, model1, metadata_file_esm, runtime_file_esm)

    model2="af2"
    metadata_file_af2 = output_dir+"/pdb_metadata_esm.tsv"
    runtime_file_af2=None
    results_to_tsv(tmalign_folder, output_dir, model2, metadata_file_af2, runtime_file_af2)

    model3="af3"
    metadata_file_af3 = output_dir+"/pdb_metadata_af2.tsv"
    runtime_file_af3= home_dir+"/02_folding/af3/af3_runtime.csv"
    results_to_tsv(tmalign_folder, output_dir, model3, metadata_file_af3, runtime_file_af3)

if __name__ == "__main__":
    main()