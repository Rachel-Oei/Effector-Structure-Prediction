import os
import re
import pandas as pd

# Write this in a function so you can use it for both ESMFold and AF3

tmalign_dir = "/home/rachel/TM-align/results2"
metadata_file = "/home/rachel/TM-align/pdb_metadata_with_tmalign_AF2.tsv"
output_file = "/home/rachel/TM-align/pdb_metadata_with_tmalign_AF3.tsv"


# -------------------------
# Read metadata table
# -------------------------

df = pd.read_csv(metadata_file, sep="\t")


# -------------------------
# Parse TM-align files
# -------------------------

results = []

for filename in os.listdir(tmalign_dir):

    if not filename.endswith("_tmalign.txt"):
        continue

    pdb_id = filename.replace("_tmalign.txt", "")

    filepath = os.path.join(tmalign_dir, filename)

    with open(filepath, "r") as f:
        text = f.read()


    # Extract values

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

    tm_AF3 = re.search(
    r"TM-score=\s+([\d.]+)\s+\(if normalized by length of Chain_1\)",
    text
)

    tm_crystal = re.search(
    r"TM-score=\s+([\d.]+)\s+\(if normalized by length of Chain_2\)",
    text
)

    pred_length = re.search(
    r"Length of Chain_1:\s+(\d+)",
    text
    )

    exp_length = re.search(
    r"Length of Chain_2:\s+(\d+)",
    text
    )

    results.append({
    "PDB_ID": pdb_id,
    "TM_score_crystal": float(tm_crystal.group(1)) if tm_crystal else None,
    "TM_score_AF3": float(tm_AF3.group(1)) if tm_AF3 else None,
    "RMSD": float(rmsd.group(1)) if rmsd else None,
    "Aligned_length": int(aligned_length.group(1)) if aligned_length else None,
    "Seq_ID": float(seq_id.group(1)) if seq_id else None,
    "ESMFold_length": int(pred_length.group(1)) if pred_length else None,
    "Experimental_length": int(exp_length.group(1)) if exp_length else None
})

# Convert to dataframe
tm_df = pd.DataFrame(results)


# -------------------------
# Merge with metadata
# -------------------------

merged = df.merge(
    tm_df,
    on="PDB_ID",
    how="left"
)


# -------------------------
# Save


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
    "TM_score_AF3",
    "RMSD",
    "Aligned_length",
    "Seq_ID"
])
