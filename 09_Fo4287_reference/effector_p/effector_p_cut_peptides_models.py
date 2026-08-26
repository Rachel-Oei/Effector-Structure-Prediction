import os 

# Read file once and create dictionary with every protein_id and their cleavage length 
def cleavage_length_dict(signal_p_file):
    cleav_length={}
    with open (signal_p_file, "r") as f:
        for line in f:
            if line.startswith("#"):    # Don't look at first line 
                continue
            columns = line.split("\t")  
            protein_id=columns[0]
            end=int(columns[4])
            cleav_length[protein_id]=end
    return cleav_length

def create_name_cut_sequence_dict (multi_fasta_file, signal_p_file):
    """
    Input is a multifasta of each protein and their cut amino acid sequences.
    Returns a dictionary containing name change 
    >AJ516_race4.FUN_002745-T1 FUN_002745
    """
    cleav_length=cleavage_length_dict(signal_p_file)

    with open (multi_fasta_file, "r") as f:
        proteins=f.read().split(">")    # split the sequences
        protein_info={}     # create dictionary to store 
        for protein in proteins:
            if protein.strip() == "":       # the first item is empty because of the split by ">", remove this
                continue
            split_fasta=protein.split("\n") # split each fasta by the lines 
            name_protein=split_fasta[0]     # the first line is always the name 
            sequence="".join(split_fasta[1:])      # join the remaining lines 
            if name_protein not in cleav_length:    # do not write a fasta file if there is no cleavage length
                continue
            num_bases_cut=cleav_length[name_protein]
            cut_sequence=sequence[num_bases_cut:]
            protein_info[name_protein]=cut_sequence    # append the cut sequence info to each name of the protein

    return protein_info

def write_single_fastas(multi_fasta_file, signal_p_file, output_fasta_dir):
    protein_info=create_name_cut_sequence_dict (multi_fasta_file, signal_p_file)
    for protein in protein_info.keys():
        output_file = f"{output_fasta_dir}/{protein}.fasta"

        # If it already exists then skip
        if os.path.exists(output_file):
            print(f"Skipping {protein}: already exists")
            continue

        with open (output_file, "w") as f:
            f.write(f">{protein}\n")
            f.write(protein_info[protein] + "\n")

        print(f"Completed {protein}.fasta")