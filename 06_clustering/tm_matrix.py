import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt

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
        matrix.loc[row["query"], row["target"]] = row["alntmscore"]

    # make symmetric
    matrix = (matrix + matrix.T) / 2

    return matrix

def plot_umap (matrix):
    distance = 1 - matrix.values

    reducer = umap.UMAP(
        metric="precomputed",
        n_neighbors=15,
        min_dist=0.1,
        random_state=42
    )

    embedding = reducer.fit_transform(distance)

    plt.figure(figsize=(8,8))

    plt.scatter(
        embedding[:,0],
        embedding[:,1],
        s=20
    )

    plt.xlabel("UMAP 1")
    plt.ylabel("UMAP 2")
    plt.title("Foldseek structural similarity landscape")

    plt.show()
