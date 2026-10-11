from cluster_visualisation_models import tree_construction, PCoA_construction

def main():

    tree_construction("effector_p", "esm")
    tree_construction("foec_2", "esm")
    PCoA_construction("effector_p", "esm")
    PCoA_construction("foec_2", "esm")


if __name__ == "__main__":
    main()