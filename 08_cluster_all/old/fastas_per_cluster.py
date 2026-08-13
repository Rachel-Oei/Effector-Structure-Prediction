

output_dir="/home/rachel/07_fold_all/foec_2/clusters"
hits_out_table="/home/jasper/NOBINFBACKUP/Fola_project/Gene_annotations/FoEC2_pangenome_effectors/output/03.presenceabsence/00_genome_effector_hits.out"

for file in /home/rachel/*07_fold_all*/old/old_foec_2/p_effector_*.afa; do
    name=$(basename "$file" .afa)
    mkdir -p "/home/rachel/07_fold_all/foec_2/clusters/$name"
done
