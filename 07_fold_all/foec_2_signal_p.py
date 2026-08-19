import os 
import subprocess 

# This is for Foec_2 Pipeline
# # Signal P 6.0. Runs by default on CPU.

# Directory of the fasta folders per cluster is: 
cluster_nuc_dir="/home/rachel/07_fold_all/foec_2/clusters"

# Naming of folders is 'cluster_109.fasta', 'multicluster_271.fasta' etc. 
# Contents of 'multicluster_271.fasta' is:

# >JAJGYP010000019.1-rna:1527
# atgTTGCCGCGGTGTGTATTTCTTGGCGTTGTATATTTGTCTATTGCTACTACTAGAAGCCCTTTG
# AAATACTTATACCCTCTTACTTCCCTTGACTTTTCATTTGactctcatcctcatcattaCCTTTGT
# TTC
# >WJXY01000229.1-rna:667
# atgTTGCCGCGGTGTGTATTTCTTGGCGTTGTATATTTGTCTATTGCTACTACTAGAAGCCCTTTG
# AAATACTTATACCCTCTTACTTCCCTTGACTTTTCATTTGactctcatcctcatcattaCCTTTGT
# TTC

all_aa_fasta="/home/rachel/07_fold_all/foec_2/all_putative_effectors_protein.fasta"
# >JAMSDW010000194.1-rna:854
# MASMSFKSIAILTFAVLQPAHGAVFPSNIFNRSEIEAMPLEKRGSMDAYQLWDSAEIPYILQSLPHDLS
# ESIRSAMREWEQSTCIRFLPKTTQSAWANFKKVSCLVPWLKTGRSRLAVR
# >JAMSDW010000230.1-rna:1126
# MKLLAVVATVLAVFSTAEAQTAQVQRHFSQTPSVDQRGAGGYDGYSQVSRPATKQGICEECRRVSDAAA
# AK

cluster_list_txt="/home/rachel/07_fold_all/foec_2/Final_clusters_list.txt"
# Some of the clusters are putative TE's so we want to exclude those.

# Sample of list of clusters to keep is:
# p_effector_613
# p_effector_493
# p_effector_45
# p_effector_592
# p_effector_13
# p_effector_36
# p_effector_495
# p_effector_290
# p_effector_335

# The p_effector_n corresponds to the cluster_n naming. E.g p_effector_613 belongs to cluster_613 in the fasta files/
with open (all_aa_fasta, "r") as f:
    proteins=f.read().split(">")
    protein_info={}
    for protein in proteins:
        if protein.strip() == "":
            continue
        split_fasta=protein.split("\n")
        name_protein=split_fasta[0]
        sequence="".join(split_fasta[1:])
        protein_info[name_protein]=sequence

cluster_filtered_dir="/home/rachel/07_fold_all/foec_2/clusters_filtered"
os.makedirs(cluster_filtered_dir, exist_ok=True)

for filename in os.listdir(cluster_nuc_dir):
    if filename.startswith("multicluster_"):
        cluster_name = filename.replace("multicluster_", "cluster_")
        with open (filename, "r") as f:
            

    with open(cluster_list_txt, "r") as f:
        for line in f:
            line = line.strip()
            cluster_number=int(line[11:])
            name= f"cluster_{cluster_number}.fasta"

            if name == cluster_name:
                with open(os.path.join(cluster_nuc_dir, filename), "r") as infile:
                    nucl_info={}
                    for line in infile:
                        if protein.strip() == "":
                            continue
                        split_fasta=line.split("\n")
                        name_protein=split_fasta[0]
                        sequence="".join(split_fasta[1:])
                        nucl_info[name_protein]=sequence
                        for nucl_name, nucl_sequence in nucl_info:
                            final_dict={}
                            for name, sequence in protein_info:
                                if nucl_name == name:
                                    final_dict[nucl_name]=sequence
                                    with open(os.path.join(cluster_filtered_dir, name), "w") as outfile:
                                        outfile.write(f">{nucl_name}\n")
                                        outfile.write(sequence + "\n")
                                else:
                                    continue 
                                
# File1: 
# >JAMSDW010000194.1-rna:854
# MASMSFKSIAILTFAVLQPAHGAVFPSNIFNRSEIEAMPLEKRGSMDAYQLWDSAEIPYILQSLPHDLS
# ESIRSAMREWEQSTCIRFLPKTTQSAWANFKKVSCLVPWLKTGRSRLAVR

# File2:
# >JAMSDW010000230.1-rna:1126
# MKLLAVVATVLAVFSTAEAQTAQVQRHFSQTPSVDQRGAGGYDGYSQVSRPATKQGICEECRRVSDAAA
# AK

out_dir = "/home/rachel/07_fold_all/foec_2/single_cut_fasta"
os.makedirs(out_dir, exist_ok=True)

model_dir = "/home/rachel/07_fold_all/signalp6_slow_sequential/signalp-6-package/models"

for filename in os.listdir(cluster_filtered_dir):

    if filename.endswith(".fasta"):

        cluster_name = filename.replace(".fasta", "")

        fasta_file = os.path.join(cluster_filtered_dir, filename)

        cluster_out_dir = os.path.join(out_dir, cluster_name)

        os.makedirs(cluster_out_dir, exist_ok=True)

        subprocess.run([
            "signalp6",
            "--model_dir", model_dir,
            "--fastafile", fasta_file,
            "--organism", "eukarya",
            "--output_dir", cluster_out_dir,
            "--format", "txt",
            "--mode", "slow-sequential"
            ], check=True)


# STILL NEED TO CONVERT NUCLEOTIDE TO AA SEQEUENCE.