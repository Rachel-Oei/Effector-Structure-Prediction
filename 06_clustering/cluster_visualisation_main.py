from cluster_visualisation_models import visualisation_pipeline

def main():
    
    folder="06_clustering"

    visualisation_pipeline(folder, "esm", 0, 0.5)

    visualisation_pipeline(folder, "af2", 0, 0.5)

    visualisation_pipeline(folder, "af3", 0, 0.5)
    
if __name__ == "__main__":
    main()