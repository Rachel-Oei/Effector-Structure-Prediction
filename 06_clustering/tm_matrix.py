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
        min_dist=0.0,
        random_state=42
    )

    embedding = reducer.fit_transform(distance)

    return embedding

def plot_umap_clusters (clusters_dir, embedding, matrix, title, n_clusters, cluster_names=None):
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

        if len(indices) <= n_clusters:
            continue

        x = embedding[indices, 0].mean()
        y = embedding[indices, 1].mean()

        label = cluster_names.get(
            str(cluster),
            str(cluster)
        )

        plt.text(
            x,
            y,
            label,
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

def order_by_clusters(matrix, clusters_dir):
    """
    Reorder the matrix so proteins belonging to the same
    Foldseek cluster are grouped together.
    """

    clusters = pd.read_csv(
        clusters_dir,
        sep="\t",
        header=None,
        names=["cluster", "protein"]
    )

    # Keep only proteins that occur in the matrix
    clusters = clusters[
        clusters["protein"].isin(matrix.index)
    ].copy()

    # Number of members in each cluster
    cluster_sizes = clusters["cluster"].value_counts()

    # Sort clusters:
    # largest clusters first
    cluster_order = (
        cluster_sizes
        .sort_values(ascending=False)
        .index
    )

    ordered_proteins = []

    for cluster in cluster_order:

        members = clusters.loc[
            clusters["cluster"] == cluster,
            "protein"
        ].tolist()

        ordered_proteins.extend(members)

    matrix_ordered = matrix.loc[
        ordered_proteins,
        ordered_proteins
    ]

    return matrix_ordered, clusters

def plot_tm_heatmap(
    matrix,
    clusters,
    font_size,
    title,
    min_cluster_size=4,
    cluster_names=None,
):
    if cluster_names is None:
        cluster_names = {}

    cluster_map = dict(
        zip(
            clusters["protein"],
            clusters["cluster"]
        )
    )

    # Cluster corresponding to each row/column
    protein_clusters = [
        cluster_map.get(protein, "Unclustered")
        for protein in matrix.index
    ]

    # --------------------------------------------------
    # Create figure
    # --------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(12, 10)
    )

    im = ax.imshow(
        matrix.values,
        cmap="Blues",
        vmin=0,
        vmax=1,
        aspect="equal"
    )

    ax.set_xticks(np.arange(len(matrix)))
    ax.set_yticks(np.arange(len(matrix)))

    ax.set_xticklabels(
        matrix.columns,
        rotation=90,
        fontsize=6
    )

    ax.set_yticklabels(
        matrix.index,
        fontsize=6
    )

    ax.set_xlabel("Target")
    ax.set_ylabel("Query")

    cbar = fig.colorbar(
        im,
        ax=ax,
        fraction=0.046,
        pad=0.04
    )

    cbar.set_label(
        "Query TM-score"
    )

    # --------------------------------------------------
    # Draw cluster boundaries
    # --------------------------------------------------

    boundaries = []

    current_cluster = protein_clusters[0]
    start = 0

    for i, cluster in enumerate(
        protein_clusters + [None]
    ):

        if cluster != current_cluster:
            end = i

            # Draw boundary around cluster
            ax.axhline(
                start - 0.5,
                linewidth=1.5
            )

            ax.axhline(
                end - 0.5,
                linewidth=1.5
            )

            ax.axvline(
                start - 0.5,
                linewidth=1.5
            )

            ax.axvline(
                end - 0.5,
                linewidth=1.5
            )

            boundaries.append(
                (start, end, current_cluster)
            )

            start = i
            current_cluster = cluster

    # --------------------------------------------------
    # Add cluster labels
    # --------------------------------------------------

    for start, end, cluster in boundaries:

        cluster_size = end - start

        # Only label clusters with >= 4 members
        if cluster_size < min_cluster_size:
            continue

        # Manual name if supplied
        label = cluster_names.get(
            str(cluster),
            str(cluster)
        )

        centre = (start + end - 1) / 2

        # Label above the heatmap
        ax.text(
            centre,
            -1.5,
            label,
            ha="center",
            va="bottom",
            fontsize=font_size,
            fontweight="bold"
        )

    ax.set_title(
    title,
    pad=30
    )

    plt.tight_layout()

    plt.show()
