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
    distance = 1 - matrix.to_numpy()

    # Force the diagonal to be 0 
    distance[distance < 0] = 0

    reducer = umap.UMAP(
        metric='precomputed',
        n_neighbors=30,
        min_dist=0.1,
        random_state=42
    )

    embedding = reducer.fit_transform(distance)

    return embedding

def plot_umap_clusters (clusters_dir, embedding, matrix, title):
    clusters = pd.read_csv(
        clusters_dir,
        sep="\t",
        header=None,
        names=["cluster","protein"]
    )

    cluster_map = dict(
        zip(
            clusters["protein"],
            clusters["cluster"]
        )
    )

    colors = [
        cluster_map[p]
        for p in matrix.index
    ]

    plt.figure(figsize=(8,8))

    plt.scatter(
        embedding[:,0],
        embedding[:,1],
        c=pd.factorize(colors)[0],
        s=30
    )

    plt.xlabel("UMAP 1")
    plt.ylabel("UMAP 2")
    plt.title(title)

    plt.show()