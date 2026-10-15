import pandas as pd
import numpy as np
from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
from Bio import Phylo
from sklearn.manifold import ClassicalMDS
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D


def tm_matrix (folder, folding_method, threshold):

    foldseek_dir=f"/home/rachel/{folder}/{folding_method}/foldseek_output/{folding_method}_foldseek_results.tsv"
    
    df = pd.read_csv(
        foldseek_dir,
        sep="\t",
        names=["query","target","alnlen","alntmscore","qtmscore", "ttmscore","rmsd"]
    )

    df = df[df["qtmscore"] >= threshold]

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

def tree_construction(folder, folding_method, threshold):

    matrix, distance = tm_matrix (folder, folding_method, threshold)

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
        f"/home/rachel/{folder}/{folding_method}/foldseek_output/{folding_method}_clusters_cluster.tsv",
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
        
    output_file=f"/home/rachel/{folder}/{folding_method}/{folding_method}_foldseek_structural_tree_threshold_{threshold}.nwk"
    Phylo.write(tree, output_file, "newick")

def PCoA_construction(folder, folding_method, threshold):
    matrix, distance = tm_matrix (folder, folding_method, threshold)

    n_proteins = len(matrix.index)

    cmds = ClassicalMDS(n_components=2, metric="precomputed")
    coordinates_cmds = cmds.fit_transform(distance)

    plt.figure(figsize=(6, 5))
    plt.scatter(coordinates_cmds[:, 0], coordinates_cmds[:, 1], color='teal', s=20)

    plt.title(f"PCoA Plot {folder} {folding_method} (qtmscore ≥ {threshold}) n_proteins={n_proteins}")
    plt.xlabel("Coordinate 1")
    plt.ylabel("Coordinate 2")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    output_file = (
    f"/home/rachel/{folder}/{folding_method}/"
    f"{folding_method}_PCoA_threshold_{threshold}.png")

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

def neural_network(folder, folding_method, threshold):
    """
    Creation of neural network
        Folder is a string of either: "10_cluster_reference", "08_cluster_all" or "09_Fo4287_reference". 
        Pipeline is a string of either: "effector_p", or "foec_2"
        Folding method is a string of either: "esm", "af2", "af3"
        Threshold1 is the first threshold for the TM score, usually >= 0.0
        Threshold2 is the second threshold for the TM score, usually >= 0.5 
    
    """
    # Read tsv
    metadata = pd.read_csv(
        "/home/rachel/04_results_tsv/pdb_metadata_af3.tsv",
        sep="\t"
    )

    def simplify_family(family):
        family = str(family).strip()
        return family if family in families else "Other"

    # Choose structural families to color 
    families = {
        "AvrSr35-like",
        "FOLD",
        "KP4-like",
        "LARS",
        "MAX",
        "RALPH",
        "ToxA-like",
    }

    metadata["Structural_family_simplified"] = metadata[
        "Structural family (inferred from La Naour Vernet et al. (2025))"
    ].apply(simplify_family)

    family_order = [
            "AvrSr35-like",
            "FOLD",
            "KP4-like",
            "LARS",
            "MAX",
            "RALPH",
            "ToxA-like",
            "Other"
    ]
    
    colors = plt.cm.tab10.colors
    category_colors = {
        category: colors[i % len(colors)]
        for i, category in enumerate(family_order)
    }

    metadata["PDB_ID"] = metadata["PDB_ID"].astype(str).str.strip()

    protein_to_family = dict(
            zip(
                metadata["PDB_ID"],
                metadata["Structural_family_simplified"]
            )
        )
    
    G = nx.Graph()

    foldseek_dir=f"/home/rachel/{folder}/{folding_method}/foldseek_output/{folding_method}_foldseek_results.tsv"
    
    df = pd.read_csv(
        foldseek_dir,
        sep="\t",
        names=["query","target","alnlen","alntmscore","qtmscore", "ttmscore","rmsd"]
    )

    for _, row in df.iterrows():

        score = row["qtmscore"]

        if (
        row["query"] != row["target"]
        and score >= threshold
    ):

            G.add_edge(
                row["query"],
                row["target"],
                weight=score
            )

    components = list(nx.connected_components(G))
    print(f"Threshold: {threshold}")
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")

    # Node colors
    node_colors = []

    for node in G.nodes():

        family = protein_to_family.get(node, "Other")

        node_colors.append(
            category_colors.get(
                family,
                category_colors["Other"]
            )
        )


    plt.figure(figsize=(12, 12))

    pos = nx.spring_layout(
        G,
        seed=42,
        weight="weight"
    )

    nx.draw(
        G,
        pos,
        node_color=node_colors,
        node_size=20,
        width=0.2,
        with_labels=False
    )

    # Legend
    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=family,
            markerfacecolor=color,
            markersize=8
        )
        for family, color in category_colors.items()
    ]

    plt.legend(
        handles=legend_handles,
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.title(
        f"Protein similarity network {folder} {folding_method} (qtmscore ≥ {threshold})"
    )

    plt.figtext(
        0.5,               # centered horizontally
        0.01,              # near bottom of figure
        f"Nodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()}",
        ha="center",
        fontsize=10
        )

    plt.subplots_adjust(bottom=0.08, right=0.8)  # leave space at bottom

    output_file = (
    f"/home/rachel/{folder}/{folding_method}/"
    f"{folding_method}_network_threshold_{threshold}.png"
    )

    plt.savefig(output_file, dpi=300)
    plt.close()

def visualisation_pipeline(folder, folding_method, threshold1, threshold2):
    """
    Tree reconstruction, PCoA and the neural network.
        Folder is a string of either: "10_cluster_reference", "08_cluster_all" or "09_Fo4287_reference". 
        Pipeline is a string of either: "effector_p", or "foec_2"
        Folding method is a string of either: "esm", "af2", "af3"
        Threshold1 is the first threshold for the TM score, usually >= 0.0
        Threshold2 is the second threshold for the TM score, usually >= 0.5 
    """
    tree_construction(folder, folding_method, threshold1)
    tree_construction(folder, folding_method, threshold2)

    PCoA_construction(folder, folding_method, threshold1)
    PCoA_construction(folder, folding_method, threshold2)

    neural_network(folder, folding_method, threshold1)
    neural_network(folder, folding_method, threshold2)
