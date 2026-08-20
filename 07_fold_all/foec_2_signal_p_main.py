from foec_2_signal_p_models import (write_cluster_fastas,
                                    signal_p,
                                    move_fastas
                                    )
import os 

def main():

    all_aa_fasta="/home/rachel/07_fold_all/foec_2/all_putative_effectors_protein.fasta"
    cluster_list_txt="/home/rachel/07_fold_all/foec_2/Final_clusters_list.txt"

    cluster_nuc_dir="/home/rachel/07_fold_all/foec_2/clusters"

    cluster_filtered_dir="/home/rachel/07_fold_all/foec_2/clusters_filtered"
    os.makedirs(cluster_filtered_dir, exist_ok=True)

    out_dir = "/home/rachel/07_fold_all/foec_2/signal_p_output"
    os.makedirs(out_dir, exist_ok=True)

    model_dir = "/home/rachel/07_fold_all/signalp6_slow_sequential/signalp-6-package/models"

    final_clusters_dir = "/home/rachel/07_fold_all/foec_2/single_cut_fasta"

    write_cluster_fastas (all_aa_fasta, 
                          cluster_list_txt, 
                          cluster_nuc_dir, 
                          cluster_filtered_dir
                          )
    
    signal_p(out_dir, 
            cluster_filtered_dir, 
            model_dir
            )

    move_fastas(out_dir, 
                final_clusters_dir, 
                cluster_filtered_dir
                )

if __name__ == "__main__":
    main()