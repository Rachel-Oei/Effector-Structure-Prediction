# This is for Foec_2 Pipeline 

# Directory of the fasta folders per cluster is: 
# fasta_dir=/home/rachel/07_fold_all/foec_2/clusters

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

# The corresponding amino acid sequences are inside 
# >JAMSDW010000194.1-rna:854
# MASMSFKSIAILTFAVLQPAHGAVFPSNIFNRSEIEAMPLEKRGSMDAYQLWDSAEIPYILQSLPHDLS
# ESIRSAMREWEQSTCIRFLPKTTQSAWANFKKVSCLVPWLKTGRSRLAVR
# >JAMSDW010000230.1-rna:1126
# MKLLAVVATVLAVFSTAEAQTAQVQRHFSQTPSVDQRGAGGYDGYSQVSRPATKQGICEECRRVSDAAA
# AK

# The list of all the effectors to keep is inside 
# clusters_list_txt=/home/rachel/07_fold_all/foec_2/Final_clusters_list.txt
# p_effector_613
# p_effector_493
# p_effector_45
# p_effector_592
# p_effector_13
# p_effector_36
# p_effector_495
# p_effector_290
# p_effector_335

# Some of these clusters are putative TE's so we want to exclude those.
# The list of clusters to keep is:
# list_clusters_txt=/home/rachel/07_fold_all/foec_2/

# Run signal_p to see where the peptides start and end. Cut the peptides.
