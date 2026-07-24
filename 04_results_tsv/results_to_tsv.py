import os 
import re
import pandas as pd

def results_to_tsv (model):

    home_dir="/home/rachel"

    if model=="esm":
        metadata_file = f"{home_dir}/04_results_tsv/pdb_metadata_with_dates.tsv"
    elif model=="af2":
        metadata_file = f"{home_dir}/04_results_tsv/pdb_metadata_esm.tsv"
    elif model=="af3":
        metadata_file = f"{home_dir}/04_results_tsv/pdb_metadata_af2.tsv"

    tmalign_dir = f"{home_dir}/03_tm_align/results_{model}"
    output_file = f"{home_dir}/04_results_tsv/pdb_metadata_{model}.tsv"

    df = pd.read_csv(metadata_file, sep="\t")

    results = []

    for filename in os.listdir(tmalign_dir):
        if filename.endswith("_tmalign.txt"):
            pdb_id = filename.replace("_tmalign.txt", "")
        elif filename.endswith(".txt"):
            pdb_id = filename.replace(".txt", "")
        else:
            continue

        filepath = os.path.join(tmalign_dir, filename)

        with open(filepath, "r") as f:
            text = f.read()

        aligned_length = re.search(
            r"Aligned length=\s+(\d+)",
            text
        )

        rmsd = re.search(
            r"RMSD=\s+([\d.]+)",
            text
        )

        seq_id = re.search(
            r"Seq_ID=n_identical/n_aligned=\s+([\d.]+)",
            text
        )

        tm_pred = re.search(
            r"TM-score=\s+([\d.]+)\s+\((?:normalized by length of Structure_1:|if normalized by length of Chain_1\))",
            text
        )

        tm_crystal = re.search(
            r"TM-score=\s+([\d.]+)\s+\((?:normalized by length of Structure_2|if normalized by length of Chain_2\))",
            text
        )

        pred_length = re.search(
            r"Length of (?:Structure_1|Chain_1):\s+(\d+)",
            text
        )

        exp_length = re.search(
            r"Length of (?:Structure_2|Chain_2):\s+(\d+)",
            text
        )

        results.append({
        "PDB_ID": pdb_id,
        "TM_score_crystal": float(tm_crystal.group(1)) if tm_crystal else None,
        "TM_score_pred": float(tm_pred.group(1)) if tm_pred else None,
        "RMSD": float(rmsd.group(1)) if rmsd else None,
        "Aligned_length": int(aligned_length.group(1)) if aligned_length else None,
        "Seq_ID": float(seq_id.group(1)) if seq_id else None,
        "Fold_length": int(pred_length.group(1)) if pred_length else None,
        "Experimental_length": int(exp_length.group(1)) if exp_length else None
    })

    tm_df = pd.DataFrame(results)

    merged = df.merge(
        tm_df,
        on="PDB_ID",
        how="left"
    )

    merged.to_csv(
        output_file,
        sep="\t",
        index=False
    )

    print("Finished!")
    print(f"Saved to: {output_file}")

    print("\nAdded columns:")
    print([
    "TM_score_crystal",
    "TM_score_pred",
    "RMSD",
    "Aligned_length",
    "Seq_ID",
    "Fold_length",
    "Experimental_length",
    ])

