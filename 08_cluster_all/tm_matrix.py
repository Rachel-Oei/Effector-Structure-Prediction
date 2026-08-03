import pandas as pd
import numpy as np
import umap 
import matplotlib.pyplot as plt

def tm_matrix (foldseek_dir):
    df = pd.read_csv(
        foldseek_dir,
        sep="\t",
        names=["query","target","alnlen","alntmscore","qtmscore", "ttmscore","rmsd"]
    )

    # Collecting all the proteins in the query and target, and sorting them
    proteins = sorted(set(df["query"]).union(df["target"]))

    # Create an identity matrix with length of n(proteins) x n(proteins)
    matrix = pd.DataFrame(
        np.eye(len(proteins)),
        index=proteins,
        columns=proteins
    )

    # From:  
    #  query    target    alntmscore
    #     A        B         0.72
    #     A        C         0.31
    #     B        A         0.68
    #     B        C         0.45

    # Convert to: 
    #           A      B      C
    #  A     1.00   0.72   0.31
    #  B     0.68   1.00   0.45
    #  C     0.??   0.??   1.00

    for _, row in df.iterrows():
        matrix.loc[row["query"], row["target"]] = row["qtmscore"]

    # Make symmetric by averaging in both normal and transposed directions 
    matrix = (matrix + matrix.T) / 2

    return matrix

def plot_umap (matrix):
    # Subtract 1 because the higher the TMscore, the lower the distance should be 
    distance = 1 - matrix.to_numpy()

    # Force the diagonal to be 0 
    distance[distance < 0] = 0

    reducer = umap.UMAP(
        metric='precomputed',
        n_neighbors=15,
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

    # Convert cluster labels to numeric values for plotting
    cluster_numbers = pd.factorize(colors)[0]

    plt.figure(figsize=(7,7))

    plt.scatter(
        embedding[:,0],
        embedding[:,1],
        c=cluster_numbers,
        s=30
    )

    # Add cluster labels at the centre of each cluster
    for cluster in sorted(set(colors)):
        indices = [
            i for i, c in enumerate(colors)
            if c == cluster
        ]

        if len(indices) <= 3:
            continue

        x = embedding[indices, 0].mean()
        y = embedding[indices, 1].mean()

        plt.text(
            x,
            y,
            str(cluster),
            fontsize=12,
            fontweight="bold",
            ha="center",
            va="center",
            bbox=dict(
                facecolor="white",
                edgecolor="none",
                alpha=0.7
            )
        )

    plt.xlabel("UMAP 1")
    plt.ylabel("UMAP 2")
    plt.title(title)

    plt.show()