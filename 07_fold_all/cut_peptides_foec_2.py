import os 

multi_fasta_dir="/home/rachel/07_fold_all/foec_2/multi_fasta"
single_fasta_dir="/home/rachel/07_fold_all/foec_2/single_fasta"
output_fasta_dir="/home/rachel/07_fold_all/foec_2/single_cut_fasta"

signal_p_dir="/home/rachel/07_fold_all/foec_2/signal_p"

for filename in os.listdir(multi_fasta_dir):
    id = filename.replace("_08_putative_effectors_protein.fasta", "") # Example: GCA_000259975

    # Find corresponding signal_p gff file 
    signal_p_specific = f"{signal_p_dir}/{id}_02_signalp.gff3"
    
    # Read file once and create dictionary with every protein_id and their cleavage length 
    cleav_length={}
    with open (signal_p_specific, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            columns = line.split("\t")
            protein_id=columns[0]
            end=int(columns[4])
            cleav_length[protein_id]=end

    for fasta in os.listdir(single_fasta_dir):
        fasta_name=fasta.replace(".fasta", "") # Example: GCA_000259975_FUN_014213

        output_file = f"{output_fasta_dir}/{fasta_name}.fasta"

        # If it already exists then skip
        if os.path.exists(output_file):
            print(f"Skipping {fasta_name}: already exists")
            continue

        # Only open fasta files with the same id
        if not fasta.startswith(f"{id}"):
            continue 

        fasta_path = f"{single_fasta_dir}/{fasta}"

        with open (fasta_path, "r") as f:
            lines = f.read().splitlines()

        header = lines[0]
        fasta_sequence= "".join(lines[1:])
        protein_id = header.replace(">", "")

        # Some fasta files have names like "Fola1_chr5-gene:775.t1", although the signal p gff says Fola1_chr5-rna:775
        signalp_id = protein_id.replace("-gene:", "-rna:")
        signalp_id = signalp_id.replace(".t1", "")

        if protein_id in cleav_length:
            num_residues_cut = cleav_length[protein_id]

        elif signalp_id in cleav_length:
            num_residues_cut = cleav_length[signalp_id]

        chain_sequence = fasta_sequence[num_residues_cut:]

        with open (output_file, "w") as f:
            f.write(f"{header}\n")
            f.write(chain_sequence + "\n")

        print(f"Completed {fasta_name}.fasta")
        print(f"(removed residues 1-{num_residues_cut})")