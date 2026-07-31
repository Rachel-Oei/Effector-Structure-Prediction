import os 

# Move all the text files with the annotations over to my own directory 

# ANNOT_DIR="/home/rachel/07_fold_all/effector_p/annotations/"
# mkdir -p ${ANNOT_DIR}
# cp /home/jasper/NOBINFBACKUP/Fola_project/Gene_annotations/EffectorP_pangenome_effectors/*/*.txt ${ANNOT_DIR}

# I will have a list of all .txt files.

annotations_dir="/home/rachel/07_fold_all/effector_p/annotations"
single_cut_fasta_dir="/home/rachel/07_fold_all/effector_p/single_cut_fasta"
output_fasta_dir="/home/rachel/07_fold_all/effector_p/effectors_fasta"

for filename in os.listdir(annotations_dir):
    id = filename.replace(".txt", "") # Example: GCA_000259975

    file=f"{annotations_dir}/{id}.txt"

    effector={}
    with open (file, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            columns = line.split("\t")
            protein_id=columns[0]
            keep_or_not=columns[4]
            effector[protein_id]=keep_or_not

    for fasta in os.listdir(single_cut_fasta_dir):
        fasta_name=fasta.replace(".fasta", "") # Example: GCA_000259975_FUN_014213
        output_file = f"{output_fasta_dir}/{fasta_name}.fasta"

        # If it already exists then skip
        if os.path.exists(output_file):
            print(f"Skipping {fasta_name}: already exists")
            continue

        # Only open fasta files with the same id
        if not fasta.startswith(f"{id}"):
            continue 

        fasta_path = f"{single_cut_fasta_dir}/{fasta}"

        with open (fasta_path, "r") as f:
            lines = f.read().splitlines()

        header = lines[0]
        fasta_sequence= "".join(lines[1:])
        protein_id = header.replace(">", "")

        if effector[protein_id]=="Non-effector":
            continue
        elif effector[protein_id]==None:
            continue
            
        with open (output_file, "w") as f:
            f.write(f"{header}\n")
            f.write(fasta_sequence + "\n")

        print(f"Completed {fasta_name}.fasta")

