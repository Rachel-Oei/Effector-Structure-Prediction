# This is for Foec_2 Pipeline
# # Signal P 6.0  

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

all_aa_dir="/home/rachel/07_fold_all/foec_2/all_putative_effectors_protein.fasta"
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

# The p_effector_n corresponds to the cluster_n naming. E.g p_effector_613 belongs to cluster_613 in the fasta files.

# Run signal_p to see where the peptides start and end. Cut the peptides.
out_dir="/home/rachel/07_fold_all/foec_2/single_cut_fasta/"

# Signal_p can have input as:
# >seq1
# ASTPGHTIIYEAVCLHNDRTTIP
# >seq2 optional comment
# ASQKRPSQRHGSKYLATASTMDHARHGFLPRHRDTGILDSIGRFFGGDRGAPK
# NMYKDSHHPARTAHYGSLPQKSHGRTQDENPVVHFFKNIVTPRTPPPSQGKGR
# KSAHKGFKGVDAQGTLSKIFKLGGRDSRSGSPMARRELVISLIVES 

# Fungi are eukaryotic organisms, short output with no graphics, slow prediction mode. 

# I would want to run the signal_p on all_aa_dir="/home/rachel/07_fold_all/foec_2/all_putative_effectors_protein.fasta"

# It will produce a gff file output. 

# 1. Create a folder for each cluster (only the ones that we want to keep)
# 2. Run signal p and get a .gff output for all 
# 3. Add amino acid fasta files that are cut to each folder. 

# How to run: 
# signalp6 --ff all_aa_dir --org eukarya --od out_dir --fmt txt --m slow-sequential
