from cluster_visualisation_models import visualisation_pipeline

def main():
    
    folder="10_cluster_reference"

    visualisation_pipeline(folder, "effector_p", "esm", 0, 0.5)
    visualisation_pipeline(folder, "foec_2", "esm", 0, 0.5)

    visualisation_pipeline(folder, "effector_p", "af2", 0, 0.5)
    visualisation_pipeline(folder, "foec_2", "af2", 0, 0.5)

    visualisation_pipeline(folder, "foec_2", "af3", 0, 0.5)
    visualisation_pipeline(folder, "effector_p", "af3", 0, 0.5)

if __name__ == "__main__":
    main()