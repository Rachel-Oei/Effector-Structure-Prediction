from cluster_visualisation_models import visualisation_pipeline
import pandas as pd

def main():
    
    folder="08_cluster_all"
    threshold1=0
    threshold2=0.5

    statistics_dict = {}

    statistics_dict.update(visualisation_pipeline(folder, "effector_p", "esm", threshold1, threshold2))
    statistics_dict.update(visualisation_pipeline(folder, "foec_2", "esm", threshold1, threshold2))

    statistics_dict.update(visualisation_pipeline(folder, "effector_p", "af2", threshold1, threshold2))
    statistics_dict.update(visualisation_pipeline(folder, "foec_2", "af2", threshold1, threshold2))

    statistics_dict.update(visualisation_pipeline(folder, "foec_2", "af3", threshold1, threshold2))
    statistics_dict.update(visualisation_pipeline(folder, "effector_p", "af3", threshold1, threshold2))

    df_statistics = pd.DataFrame(statistics_dict)

    df_statistics.to_excel(f"/home/rachel/{folder}/{folder}_network_statistics.xlsx")
    
if __name__ == "__main__":
    main()