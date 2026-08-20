from effector_p_signal_p_models import (run_signal_p,
                                    move_fastas,
                                    separate_select_fastas
                                    )
import os 

# This is for Effector_P Pipeline 

# Directory of the fasta folders per cluster is: 
# fasta_dir=/home/rachel/07_fold_all/effector_p/clusters

# Naming of folders is 'Cluster_109.fasta', 'Cluster_110.fasta' etc. 
# Contents of 'Cluster_109.fasta' is:

# >AJ516_race4.FUN_002745-T1 FUN_002745
# MKFATALVGLVASATYAAAASVTFGPESVTVSSAKEVTVDFPDKYIGNFYAVQKGKPDQPGML
# GEVTFGGWNGKTYFDVSAIVDPNDKNNVKQMWPKSAATPMSGCETFPCDNCYWLPDDVQTKVT
# DEVDLITTLGDGPSPYKAKSN
# >AJ520_race1.FUN_002739-T1 FUN_002739
# MKFATALVGLVASATYAAAASVTFGPESVTVSSAKEVTVDFPDKYIGNFYAVQKGKPDQPGML
# GEVTFGGWNGKTYFDVSAIVDPNDKNNVKQMWPKSAATPMSGCETFPCDNCYWLPDDVQTKVT
# DEVDLITTLGDGPSPYKAKSN
# >AJ592_race4.FUN_002682-T1 FUN_002682
# MKFATALVGLVASATYAAAASVTFVTLDDKERTIIFTPDPGYEGPESVTVSSAKEVTVDFPDK
# YIGNFYAVQKGKPDQPGMLGEVTFGGWNGKTYFDVSAIVDPNDKNNVKQMWPKSAATPMSGCE
# TFPCDNCYWLPDDVQTKVTDEVDLITTLGDGPSPYKAKSN

# Some of these clusters are putative TE's so, we want to exclude those.
# The list of clusters to keep is:
# list_clusters_txt=/home/rachel/07_fold_all/effector_p/Final_clusters_list.txt

def main():

    project_dir="/home/rachel/07_fold_all/effector_p"
    cluster_list_txt=f"{project_dir}/Final_clusters_list.txt"
    cluster_dir=f"{project_dir}/clusters"

    model_dir = "/home/rachel/07_fold_all/signalp6_slow_sequential/signalp-6-package/models"

    out_dir = f"{project_dir}/signal_p_output"
    os.makedirs(out_dir, exist_ok=True)

    final_clusters_dir = f"{project_dir}/single_cut_fasta"
    os.makedirs(final_clusters_dir, exist_ok=True)

    n_proteins=2    # Default number of proteins folded per cluster is 2. 
                        # If the cluster contains less, it is skipped

    select_clusters_dir=f"{project_dir}/select_separate_fasta"
    os.makedirs(select_clusters_dir, exist_ok=True)

    run_signal_p (out_dir, cluster_dir, model_dir)
    move_fastas(out_dir, cluster_dir, final_clusters_dir)
    separate_select_fastas (n_proteins, final_clusters_dir, select_clusters_dir)

if __name__ == "__main__":
    main()