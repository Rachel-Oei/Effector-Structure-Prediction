import subprocess 

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

def run_signal_p (model_dir, fasta_file, signal_p_output): 
    """
    Running SignalP for the FOEC_2 pipeline
    """
    # Run SignalP. Settings: fungi are eukaryotic organisms, short output with no graphics, slow prediction mode. 
    subprocess.run([
        "signalp6",
        "--model_dir", model_dir,
        "--fastafile", fasta_file,
        "--organism", "eukarya",
        "--output_dir", signal_p_output,
        "--format", "txt",
        "--mode", "slow-sequential"
        ], check=True)

def move_fastas(fasta_file, signal_p_output, single_cut_fasta_out):
    """
    If signal P classifies the protein as "OTHER", it does not give a peptide sequence.
    If signal P classifies it as "SP" (signal peptide), give the cut sequence 
    Output is moved to 'output_file_name': "/home/rachel/09_Foc4287_reference/foec_2/single_cut_fasta/_.fasta"
    """
    
    prediction_txt=f"{signal_p_output}/prediction_results.txt"
    signal_p_fasta=f"{signal_p_output}/processed_entries.fasta"
    signal_p_fasta_dict=create_name_sequence_dict(signal_p_fasta)
    original_fasta_dict=create_name_sequence_dict(fasta_file)

    with open (prediction_txt, "r") as f:   # Open the prediction to see what category the peptide belongs to 
        lines=f.read().split("\n")
        for line in lines:
            if line.startswith("#") or line == "":     # Do not look at the first two lines
                continue

            split_line = line.split()   # Make a list out of the columns

            protein_name = split_line[0]
            prediction = split_line[1]

            if prediction == "SP":  # If the peptide is a signal peptide 
                if protein_name in signal_p_fasta_dict:   # Then use the processed sequence from signal p
                    sequence=signal_p_fasta_dict[protein_name]
                else:
                    print(
                            f"WARNING: {protein_name} "
                            f"not found in {signal_p_fasta}"
                        )
                    continue 

            elif prediction == "OTHER":
                if protein_name in original_fasta_dict:
                    sequence=original_fasta_dict[protein_name]
                else:
                    print(
                            f"WARNING: {protein_name} "
                            f"not found in {fasta_file}"
                        )
                    continue 
            else: 
                print (f"WARNING: {protein_name} "
                        f"does not have a prediction by Signal P"
                        )
                continue 

            output_file_name=f"{single_cut_fasta_out}/{protein_name}.fasta"

            with open (output_file_name, "w") as out_f:
                out_f.write(f">{protein_name}\n")   # Write the new fasta files with the correct sequence 
                out_f.write(sequence + "\n")

            print (f"{output_file_name}: completed")