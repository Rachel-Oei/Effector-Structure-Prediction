import os 
import subprocess
import random

def create_name_sequence_dict (multifasta):
    """
    Input is a multifasta of each protein and their amino acid sequences.
    Returns a dictionary containing name change 
    >AJ516_race4.FUN_002745-T1 FUN_002745
    """
    with open (multifasta, "r") as f:
        proteins=f.read().split(">")    # split the sequences
        protein_info={}     # create dictionary to store 
        for protein in proteins:
            if protein.strip() == "":       # the first item is empty because of the split by ">", remove this
                continue
            split_fasta=protein.split("\n") # split each fasta by the lines 
            name_protein=split_fasta[0]     # the first line is always the name 
            sequence="".join(split_fasta[1:])      # join the remaining lines 
            protein_info[name_protein]=sequence    # append the sequence info to each name of the protein
    return protein_info

def create_clusters_to_keep_set (cluster_list_txt):
    """
    Returns set of clusters to keep according to the txt input.
    """
    clusters_to_keep = set()    # Initiate it as a set 
    # Make a list of all cluster files to keep in cluster_.fasta format
    with open(cluster_list_txt, "r") as f:
        for line in f:     
            line = line.strip()
            clusters_to_keep.add(line)
    return clusters_to_keep

def run_signal_p (cluster_list_txt, out_dir, cluster_dir, model_dir): 
    """
    Running SignalP for the Effector_P pipeline
    """
    clusters_to_keep=create_clusters_to_keep_set(cluster_list_txt)

    for filename in os.listdir(cluster_dir): # Loop over every file inside cluster_dir
        fasta_file = os.path.join(cluster_dir, filename)
        cluster_name = filename.replace(".fasta", "")
        cluster_out_dir = os.path.join(out_dir, cluster_name)

        signalp_output = os.path.join(cluster_out_dir, "prediction_results.txt")

        if os.path.exists(signalp_output):
            print(f"Skipping {cluster_name}: SignalP output already exists")
            continue

        if cluster_name not in clusters_to_keep:
            print(f"Skipping {cluster_name}: not in clusters to keep set")
            continue

        # Run SignalP. Settings: fungi are eukaryotic organisms, short output with no graphics, slow prediction mode. 
        subprocess.run([
            "signalp6",
            "--model_dir", model_dir,
            "--fastafile", fasta_file,
            "--organism", "eukarya",
            "--output_dir", cluster_out_dir,
            "--format", "txt",
            "--mode", "slow-sequential"
            ], check=True)

def move_fastas(signal_p_out_dir, cluster_dir, final_clusters_dir):
    """
    If signal P classifies the protein as "OTHER", it does not give a peptide sequence.
    If signal P classifies it as "SP" (signal peptide), give the cut sequence 
    Output is moved to 'final_clusters_file': "/home/rachel/07_fold_all/foec_2/single_cut_fasta/_.fasta"
    """
    for cluster in os.listdir(signal_p_out_dir): # Loop through the clusters in signal p output 
        cluster_path=os.path.join(signal_p_out_dir,cluster)

        prediction_txt=os.path.join(cluster_path,"prediction_results.txt")
        processed_entries_file=os.path.join(cluster_path,"processed_entries.fasta")

        final_clusters_file=os.path.join(final_clusters_dir,f"{cluster}.fasta")
        filtered_clusters_file=os.path.join(cluster_dir,f"{cluster}.fasta")

        with open (final_clusters_file, "w") as out_f:
            # Get dictionary with protein: sequence info 
            filtered_info=create_name_sequence_dict(filtered_clusters_file) 
            # Get dictionary with protein: sequence info processed after signal P
            signal_p_info=create_name_sequence_dict(processed_entries_file) 
            with open (prediction_txt, "r") as f:   # Open the prediction to see what category the peptide belongs to 
                lines=f.read().split("\n")
                for line in lines:
                    if line.startswith("#") or line == "":     # Do not look at the first two lines
                        continue

                    split_line = line.split()   # Make a list out of the columns

                    protein_name = split_line[0]+" "+split_line[1]
                    prediction = split_line[2]

                    if prediction == "SP":  # If the peptide is a signal peptide 
                        if protein_name in signal_p_info:   # Then use the processed sequence from signal p
                            sequence=signal_p_info[protein_name]
                        else:
                            print(
                                    f"WARNING: {protein_name} "
                                    f"not found in {processed_entries_file}"
                                )
                            continue 

                    elif prediction == "OTHER":
                        if protein_name in filtered_info:
                            sequence=filtered_info[protein_name]
                        else:
                            print(
                                    f"WARNING: {protein_name} "
                                    f"not found in {filtered_clusters_file}"
                                )
                            continue 
                    else: 
                        print (f"WARNING: {protein_name} "
                                f"does not have a prediction by Signal P"
                                )
                        continue 

                    out_f.write(f">{protein_name}\n")   # Write the new fasta files with the correct sequence 
                    out_f.write(sequence + "\n")

def choose_n_proteins_per_cluster (n_proteins, final_clusters_dir):
    """
    Choose n number of proteins per cluster in a random order. 
    Uses .random package. If the cluster contains less than the desired 
    number of proteins, it is skipped. 

    Output is dictionary with:
        {"cluster_1": ["random_protein1", "random_protein2"],
        "cluster_2": ["random_protein1", "random_protein2"],
    """
    cluster_files_dict={}
    for cluster in os.listdir(final_clusters_dir):
        cluster_name=cluster.replace(".fasta", "")
        cluster_file=f"{final_clusters_dir}/{cluster}"
        protein_dict=create_name_sequence_dict(cluster_file)

        if len(protein_dict) == 0:
            continue

        elif len(protein_dict) < n_proteins:  # If the cluster contains less than the number of proteins 
                                            # that we want, then we just take that sequence 
            print(
                f"WARNING: {cluster_name} only contains "
                f"{len(protein_dict)} proteins. We still consider this "
            )

            proteins_chosen = list(protein_dict.keys())
            cluster_files_dict[cluster_name]=proteins_chosen
            continue
        
        else: 
            proteins_chosen=random.sample(           # .sample makes sure there is no replacement 
                list(protein_dict.keys()), 
                n_proteins)    

            cluster_files_dict[cluster_name]=proteins_chosen

    return cluster_files_dict

def separate_select_fastas (n_proteins, final_clusters_dir, select_clusters_dir):
    """
    Create a folder with all the final fasta files, all separated and with naming convention:
    "effector_p_cluster_27_JAMSDW010000212.1-rna:942.fasta"
    If it already exists, skip.
    """
    cluster_files_dict=choose_n_proteins_per_cluster(n_proteins, final_clusters_dir)

    for cluster, selected_proteins in cluster_files_dict.items():   
        cluster_file=f"{final_clusters_dir}/{cluster}.fasta"    
        protein_dict=create_name_sequence_dict(cluster_file)    # Get the sequence of that cluster 

        for protein in selected_proteins:   # Loop through every selected protein of the cluster 
            fasta_file=f"{select_clusters_dir}/effector_p_{cluster.lower()}_{protein}.fasta"
            if os.path.exists(fasta_file):
                print(f"Skipping effector_p_{cluster.lower()}_{protein}.fasta: SignalP output already exists")
                continue
            sequence=protein_dict[protein]
            with open (fasta_file, "w") as f:
                f.write(f">{protein}\n")   # Write the new fasta files with the correct sequence 
                f.write(sequence + "\n")