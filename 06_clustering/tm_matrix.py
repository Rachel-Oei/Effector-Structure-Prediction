import pandas as pd
import numpy as np

def tm_matrix (foldseek_dir):
    df = pd.read_csv(
        foldseek_dir,
        sep="\t",
        names=["query","target","alnlen","alntmscore","rmsd"]
    )

    proteins = sorted(set(df["query"]).union(df["target"]))

    matrix = pd.DataFrame(
        np.eye(len(proteins)),
        index=proteins,
        columns=proteins
    )

    for _, row in df.iterrows():
        matrix.loc[row["query"], row["target"]] = row["tmscore"]

    # make symmetric
    matrix = (matrix + matrix.T) / 2

    return matrix

def umap (matrix)
