import os 
import subprocess 
import random

# This is for Foec_2 Pipeline
# # Signal P 6.0. Runs by default on CPU.

def create_name_sequence_dict (multifasta):
    """
    Input is a multifasta of each protein and their amino acid sequences.
    Returns a dictionary containing, e.g:
    {
    'JAMSDW010000194.1-rna:854': 'MASMSFKSIAILTFAVLQPAHGAVFPSNIFNRSEIEAMPLEKRGS
    MDAYQLWDSAEIPYILQSLPHDLSESIRSAMREWEQSTCIRFLPKTTQSAWANFKKVSCLVPWLKTGRSRLAVR',
    'JAMSDW010000230.1-rna:1126': 'MKLLAVVATVLAVFSTAEAQTAQVQRHFSQTPSVDQRGAGGYDGYSQ
    VSRPATKQGICEECRRVSDAAAAK'
    }
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
            line = line.strip()     # Removes spaces, tabs, or newlines from begin or end of string 
            cluster_number=int(line[11:])   # Define the cluster number by the number from the 11th character
            name= f"cluster_{cluster_number}.fasta"     # Rename the fasta file  
            clusters_to_keep.add(name)     # Add the cluster file name to the set 
    return clusters_to_keep

def write_cluster_fastas (all_aa_fasta, cluster_list_txt, cluster_nuc_dir, cluster_filtered_dir):
    """"
    Matches the nucleotide sequences to amino acid sequences, and writes new fastas.
    Input is 'cluster_list_txt', the txt file containing e.g:
        p_effector_613
        p_effector_493
        p_effector_45
        p_effector_592
        p_effector_13

        p_effector naming is consistent with cluster naming. E.g p_effector_13 
        corresponds to cluster_13.
        
        As well as the 'cluster_nuc_dir' which is a directory containing 
        folders with names e.g 'cluster_109.fasta', 'multicluster_271.fasta' etc. 
        Contents of 'multicluster_271.fasta' is:

        >JAJGYP010000019.1-rna:1527
        atgTTGCCGCGGTGTGTATTTCTTGGCGTTGTATATTTGTCTATTGCTACTACTAGAAGCCCTTTG
        AAATACTTATACCCTCTTACTTCCCTTGACTTTTCATTTGactctcatcctcatcattaCCTTTGT
        TTC
        >WJXY01000229.1-rna:667
        atgTTGCCGCGGTGTGTATTTCTTGGCGTTGTATATTTGTCTATTGCTACTACTAGAAGCCCTTTG
        AAATACTTATACCCTCTTACTTCCCTTGACTTTTCATTTGactctcatcctcatcattaCCTTTGT
        TTC

        'cluster_filtered_dir' is the directory where all the output is stored:
        "/home/rachel/07_fold_all/foec_2/clusters_filtered"

    Output is the newly written fasta files with amino acid sequences of filtered clusters.

    """
    protein_info=create_name_sequence_dict(all_aa_fasta) # Create protein info dictionary
    clusters_to_keep=create_clusters_to_keep_set(cluster_list_txt)  # Creates set of clusters to keep

    for filename in os.listdir(cluster_nuc_dir):     
        cluster_name=filename  
        if filename.startswith("multicluster_"):    
            cluster_name = filename.replace("multicluster_", "cluster_") # Rename each multicluster to cluster 
        if cluster_name not in clusters_to_keep:    # Skip if the cluster name is not in the filtered cluster set  
            continue

        # Open the cluster file 
        with open(os.path.join(cluster_nuc_dir, filename), "r") as f:
            records = f.read().split(">")     # Separate the fastas
            output_file = os.path.join(cluster_filtered_dir, cluster_name) # Create output file destination
            with open(output_file, "w") as out_f:
                # Loop through each separated fasta
                for record in records:  
                    if record.strip() == "":    # Skip the first empty
                        continue
                    lines = record.strip().split("\n")  # Remove the newlines 
                    protein_name = lines[0]    # Take the name from the first line 
                    if protein_name in protein_info:   # Check whether this matches with protein_info dictionary 
                        protein_sequence = protein_info[protein_name]   # Access the protein sequence from dictionary 
                        out_f.write(f">{protein_name}\n")   # Write the new fasta files 
                        out_f.write(protein_sequence + "\n")
                        # Keep appending the output_file until all fastas per cluster are written
                    else:
                        print(
                            f"WARNING: {protein_name} "
                            f"not found in protein FASTA"
                        )

def run_signal_p (out_dir, cluster_filtered_dir, model_dir): 
    """
    Running SignalP for the FOEC_2 pipeline
    """

    for filename in os.listdir(cluster_filtered_dir): # Loop over every file inside cluster_filtered_dir
        fasta_file = os.path.join(cluster_filtered_dir, filename)
        cluster_name = filename.replace(".fasta", "")
        cluster_out_dir = os.path.join(out_dir, cluster_name)

        signalp_output = os.path.join(cluster_out_dir, "prediction_results.txt")

        if os.path.exists(signalp_output):
            print(f"Skipping {cluster_name}: SignalP output already exists")
            continue
        
        subprocess.run([
            "signalp6",
            "--model_dir", model_dir,
            "--fastafile", fasta_file,
            "--organism", "eukarya",
            "--output_dir", cluster_out_dir,
            "--format", "txt",
            "--mode", "slow-sequential"
            ], check=True)

def move_fastas(signal_p_out_dir, final_clusters_dir, cluster_filtered_dir):
    """
    If signal P classifies the protein as "OTHER", it does not give a peptide sequence.
    If signal P classifies it as "SP" (signal peptide), give the cut sequence 
    Output is moved to 'final_clusters_dir': "/home/rachel/07_fold_all/foec_2/single_cut_fasta"
    """
    for cluster in os.listdir(signal_p_out_dir): # Loop through the clusters in signal p output 
        cluster_path=os.path.join(signal_p_out_dir,cluster)

        prediction_txt=os.path.join(cluster_path,"prediction_results.txt")
        processed_entries_file=os.path.join(cluster_path,"processed_entries.fasta")

        final_clusters_file=os.path.join(final_clusters_dir,cluster)
        filtered_clusters_file=os.path.join(cluster_filtered_dir,f"{cluster}.fasta")

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

                    protein_name = split_line[0]
                    prediction = split_line[1]

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

def choose_n_proteins_per_cluster (n_proteins, cluster_dir):
    """
    Choose n number of proteins per cluster in a random order. 
    Default is n=2. Uses .random package. 
    Output is dictionary with:
    {"cluster_1": [{"random_protein1": AA_sequence}, {"random_protein2": AA_sequence}],
    "cluster_2": [{"random_protein1": AA_sequence}, {"random_protein2": AA_sequence}]}
    """
    cluster_files_dict={}
    for cluster in os.listdir(cluster_dir):
        cluster_name=cluster.replace("fasta","")
        cluster_file=f"{cluster_dir}/{cluster_name}.fasta"
        protein_dict=create_name_sequence_dict(cluster_file)
        proteins_chosen=[]
        for i in range(n_proteins):
            i+=1
            protein_chosen=random.sample(list(protein_dict))    # .sample makes sure there is no replacement 
            proteins_chosen.append(protein_chosen)

        cluster_files_dict[cluster]=proteins_chosen

    return cluster_files_dict



