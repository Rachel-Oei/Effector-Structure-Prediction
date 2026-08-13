from fold_models import Fold

# Folds one folding method at a time. You can run multiple folding methods parallel and change gpu. 

def main():
    fold=Fold(
        pipeline="effector_p",
        folding_method="af3",
        proteins_per_cluster=3,
        gpu=1,
        json_dir="/home/rachel/07_fold_all/json",
        processed_fasta_dir="/home/rachel/07_fold_all/single_cut_fasta"
    )

    fold.run()

if __name__ == "__main__":
    main()