from foec_2_signal_p_models import (write_cluster_fastas,
                                    run_signal_p,
                                    move_fastas,
                                    choose_n_proteins_per_cluster
                                    )
import os 

def main():

    project_dir="/home/rachel/07_fold_all/foec_2"

    all_aa_fasta=f"{project_dir}/all_putative_effectors_protein.fasta"

    cluster_list_txt=f"{project_dir}/Final_clusters_list.txt"

    cluster_nuc_dir=f"{project_dir}/clusters"

    cluster_filtered_dir=f"{project_dir}/clusters_filtered"
    os.makedirs(cluster_filtered_dir, exist_ok=True)

    out_dir = f"{project_dir}/signal_p_output"
    os.makedirs(out_dir, exist_ok=True)

    model_dir = "/home/rachel/07_fold_all/signalp6_slow_sequential/signalp-6-package/models"

    final_clusters_dir = f"{project_dir}/single_cut_fasta"
    os.makedirs(final_clusters_dir, exist_ok=True)

    n_proteins=2    # Default number of proteins folded per cluster is 2. 
                    # If the cluster contains less, it is skipped

    write_cluster_fastas (all_aa_fasta, 
                          cluster_list_txt, 
                          cluster_nuc_dir, 
                          cluster_filtered_dir
                          )
    
    run_signal_p(out_dir, 
            cluster_filtered_dir, 
            model_dir
            )

    move_fastas(out_dir, 
                final_clusters_dir, 
                cluster_filtered_dir
                )

    choose_n_proteins_per_cluster (n_proteins, final_clusters_dir)

if __name__ == "__main__":
    main()