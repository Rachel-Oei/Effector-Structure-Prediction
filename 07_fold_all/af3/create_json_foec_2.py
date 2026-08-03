import json
import sys
import os 

sys.path.append("/home/rachel/01_prepare_cif")
from prepare_cif_models import create_directory

folding_directory="/home/rachel/07_fold_all/foec_2"
fasta_dir="/home/rachel/07_fold_all/foec_2/single_cut_fasta"
group_dir="/home/rachel/07_fold_all/foec_2/multi_fasta"

output_dir=folding_directory+"/af3/json"
create_directory(output_dir)

def create_json (fasta_dir, output_dir, n_files):
    """
    Reads fasta file for each protein, creates json file in the format of:
    {
      "name": "2PV7_1",
      "sequences": [
	{
	  "protein": {
            "id": ["A"],
            "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG"
	  }
	}
      ],
      "modelSeeds": [1],
      "dialect": "alphafold3",
      "version": 1
    }

    Output name is e.g 2PV7_1.json

    """    
    for group in os.listdir(group_dir):
        if group.endswith("_08_putative_effectors_protein.fasta"):
            group_name = group.replace("_08_putative_effectors_protein.fasta", "")
        else:
            continue 

        matching_fastas=[]
        for fasta_file in os.listdir(fasta_dir):
            if fasta_file.endswith(".fasta") and group_name in fasta_file:
                pdb_id = fasta_file.replace(".fasta", "")
                matching_fastas.append(fasta_file)
            else:
                continue 

        for fasta_file in matching_fastas[:int(n_files)]:
            fasta_path = os.path.join(fasta_dir, fasta_file)

            with open(fasta_path) as f:
                sequence_lines = []
                for line in f:
                    if not line.startswith(">"):
                        sequence_lines.append(line.strip())
                sequence = "".join(sequence_lines)

            json_data={
                "name":f"{pdb_id}",
                "sequences": [
                {
                    "protein": {
                    "id": ["A"],
                    "sequence": sequence
                    }
                }
                ],
                "modelSeeds": [1],
                "dialect": "alphafold3",
                "version": 1
            }
            
            output_file = f"{output_dir}/{pdb_id}.json"

            # Write the json file 
            with open(output_file, "w") as f:
                json.dump(json_data, f, indent=2)

            print(f"{pdb_id}.json created")

create_json(fasta_dir, output_dir, 3)