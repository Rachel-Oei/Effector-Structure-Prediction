import pandas as pd
import numpy as np
from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
from Bio import Phylo
from sklearn.manifold import ClassicalMDS
import matplotlib.pyplot as plt

def tm_matrix (pipeline, folding_method):

    foldseek_dir=f"/home/rachel/08_cluster_all/{pipeline}/{folding_method}/foldseek_output/{folding_method}_foldseek_results.tsv"

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

    # Subtract 1 because the higher the TMscore, the lower the distance should be 
    distance = 1 - matrix.to_numpy()
    
    # Force the diagonal to be 0 
    distance[distance < 0] = 0

    return matrix, distance

def tree_construction(pipeline, folding_method):

    matrix, distance = tm_matrix (pipeline, folding_method)

    # Protein names
    names = list(matrix.index)

    # Biopython DistanceMatrix requires the lower triangle
    lower_triangle = [
        [distance[i, j] for j in range(i + 1)]
        for i in range(len(names))
    ]

    dm = DistanceMatrix(names, lower_triangle)

    # Neighbor Joining
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(dm)

    # Labelling with clusters 
    clusters = pd.read_csv(
        f"/home/rachel/08_cluster_all/{pipeline}/{folding_method}/foldseek_output/{folding_method}_clusters_cluster.tsv",
        sep="\t",
        header=None,
        names=["cluster", "protein"]
        )
        
    protein_to_cluster = dict(
        zip(clusters["protein"], clusters["cluster"])
    )

    for leaf in tree.get_terminals():
        protein = leaf.name
        safe_protein = protein.replace(":", "_").replace(" ", "_")

        cluster = protein_to_cluster.get(protein, "Unknown")
        safe_cluster = cluster.replace(":", "_").replace(" ", "_")

        leaf.name = f"{safe_protein} | Cluster {safe_cluster}"
        

    output_file=f"/home/rachel/08_cluster_all/{pipeline}/{folding_method}/{pipeline}_{folding_method}_foldseek_structural_tree.nwk"
    Phylo.write(tree, output_file, "newick")

def PCoA_construction(pipeline, folding_method):
    matrix, distance = tm_matrix (pipeline, folding_method)
    proteins = matrix.index

    cmds = ClassicalMDS(n_components=2, metric="precomputed")
    coordinates_cmds = cmds.fit_transform(distance)

    plt.figure(figsize=(6, 5))
    plt.scatter(coordinates_cmds[:, 0], coordinates_cmds[:, 1], color='teal', s=20)

    # for i, (x, y) in enumerate(coordinates_cmds):
    #     plt.text(x, y, proteins[i], fontsize=8)

    plt.title("PCoA / Classical MDS Plot")
    plt.xlabel("Coordinate 1")
    plt.ylabel("Coordinate 2")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    output_file = (
    f"/home/rachel/08_cluster_all/{pipeline}/{folding_method}/"
    f"{pipeline}_{folding_method}_PCoA.png")

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()