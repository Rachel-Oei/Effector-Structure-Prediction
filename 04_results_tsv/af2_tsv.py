import os
import re
import pandas as pd

tmalign_dir = "/home/rachel/AF2/AlphaFold2/81_Trials/TMalign_results"

metadata_file = "/home/rachel/TM-align/pdb_metadata_with_tmalign.tsv"

output_file = "/home/rachel/TM-align/pdb_metadata_with_tmalign_AF2.tsv"


# -------------------------
# Read metadata table
# -------------------------

df = pd.read_csv(metadata_file, sep="\t")


# -------------------------
# Parse TM-align files
# -------------------------

results = []

for filename in os.listdir(tmalign_dir):

    if not filename.endswith(".txt"):
        continue

    pdb_id = filename.replace(".txt", "")

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

    tm_AF2 = re.search(
    r"TM-score=\s+([\d.]+)\s+\(normalized by length of Structure_1:",
    text
)

    tm_crystal = re.search(
    r"TM-score=\s+([\d.]+)\s+\(normalized by length of Structure_2",
    text
)

    pred_length = re.search(
    r"Length of Structure_1:\s+(\d+)",
    text
    )

    exp_length = re.search(
    r"Length of Structure_2:\s+(\d+)",
    text
    )

    results.append({
    "PDB_ID": pdb_id,
    "TM_score_crystal": float(tm_crystal.group(1)) if tm_crystal else None,
    "TM_score_AF2": float(tm_AF2.group(1)) if tm_AF2 else None,
    "RMSD": float(rmsd.group(1)) if rmsd else None,
    "Aligned_length": int(aligned_length.group(1)) if aligned_length else None,
    "Seq_ID": float(seq_id.group(1)) if seq_id else None,
    "AF2_length": int(pred_length.group(1)) if pred_length else None,
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
# -------------------------

merged.to_csv(
    output_file,
    sep="\t",
    index=False
)

print("Finished!")
print(f"Saved to: {output_file}")

print("\nAdded columns:")
print([
    "TM_crystal",
    "TM_AF2",
    "RMSD",
    "Aligned_length",
    "Seq_ID"
])

