from cluster_visualisation_models import tree_construction, PCoA_construction

def main():

    tree_construction("effector_p", "esm")
    tree_construction("foec_2", "esm")
    PCoA_construction("effector_p", "esm")
    PCoA_construction("foec_2", "esm")

    tree_construction("effector_p", "af3")
    tree_construction("foec_2", "af3")
    PCoA_construction("effector_p", "af3")
    PCoA_construction("foec_2", "af3")

    tree_construction("effector_p", "af2")
    tree_construction("foec_2", "af2")
    PCoA_construction("effector_p", "af2")
    PCoA_construction("foec_2", "af2")


if __name__ == "__main__":
    main()