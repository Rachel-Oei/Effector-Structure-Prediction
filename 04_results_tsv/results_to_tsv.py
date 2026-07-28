import os 
import re
import pandas as pd

def results_to_tsv (tmalign_folder, output_dir, model, metadata_file, runtime_file=None):
    tmalign_dir = tmalign_folder+"/results_{model}"
    output_file = output_dir+"/pdb_metadata_{model}.tsv"

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
        f"TM_score_crystal_{model}": float(tm_crystal.group(1)) if tm_crystal else None,
        f"TM_score_pred_{model}": float(tm_pred.group(1)) if tm_pred else None,
        f"RMSD_{model}": float(rmsd.group(1)) if rmsd else None,
        f"Aligned_length_{model}": int(aligned_length.group(1)) if aligned_length else None,
        f"Seq_ID_{model}": float(seq_id.group(1)) if seq_id else None,
        f"Pred_length_{model}": int(pred_length.group(1)) if pred_length else None,
        f"Experimental_length_{model}": int(exp_length.group(1)) if exp_length else None,
        f"Coverage_{model}":int(exp_length.group(1))/int(pred_length.group(1)) if pred_length and exp_length else None 
    })

    tm_df = pd.DataFrame(results)

    merged = df.merge(
        tm_df,
        on="PDB_ID",
        how="left"
    )

    # If there is no runtime file, do not collect it
    if runtime_file:
        runtime_df = pd.read_csv(runtime_file,names=["PDB_ID", f"runtime_seconds_{model}"])

        # Remove failed runs with runtime 0 or 1
        runtime_df = runtime_df[runtime_df[f"runtime_seconds_{model}"] > 1]

        merged = merged.merge(
            runtime_df,
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
    f"TM_score_crystal_{model}",
    f"TM_score_pred_{model}",
    f"RMSD_{model}",
    f"Aligned_length_{model}",
    f"Seq_ID_{model}",
    f"Fold_length_{model}",
    f"Experimental_length_{model}",
    f"Coverage_{model}",
    f"Runtime_seconds if available",
    ])