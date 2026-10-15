from cluster_visualisation_models import tree_construction, PCoA_construction, neural_network

def visualisation_pipeline(folder, pipeline, folding_method, threshold1, threshold2):
    """
    Tree reconstruction, PCoA and the neural network.
        Folder is a string of either: "10_cluster_reference", "08_cluster_all" or "09_Fo4287_reference". 
        Pipeline is a string of either: "effector_p", or "foec_2"
        Folding method is a string of either: "esm", "af2", "af3"
        Threshold1 is the first threshold for the TM score, usually >= 0.0
        Threshold2 is the second threshold for the TM score, usually >= 0.5 
    """
    tree_construction(folder, pipeline, folding_method, threshold1)
    tree_construction(folder, pipeline, folding_method, threshold2)

    PCoA_construction(folder, pipeline, folding_method, threshold1)
    PCoA_construction(folder, pipeline, folding_method, threshold2)

    neural_network(folder, pipeline, folding_method, threshold1)
    neural_network(folder, pipeline, folding_method, threshold2)

def main():

    visualisation_pipeline("10_cluster_reference", "effector_p", "esm", 0, 0.5)
    visualisation_pipeline("foec_2", "esm", 0, 0.5)

    visualisation_pipeline("effector_p", "af2", 0, 0.5)
    visualisation_pipeline("foec_2", "af2", 0, 0.5)

    visualisation_pipeline("effector_p", "af3", 0, 0.5)
    visualisation_pipeline("effector_p", "af3", 0, 0.5)

if __name__ == "__main__":
    main()