import json
import os 

def create_json (pipeline):
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
    fasta_dir=f"/home/rachel/09_Fo4287_reference/{pipeline}/single_cut_fasta"
    folding_directory=f"/home/rachel/09_Fo4287_reference/{pipeline}"
    output_dir=folding_directory+"/af3/json"
    os.makedirs(output_dir, exist_ok=True)

    for fasta_file in os.listdir(fasta_dir):
        fasta_path = os.path.join(fasta_dir, fasta_file)
        name = fasta_file.replace(".fasta", "").replace(" ", "_") # So that the name does not contain spaces

        with open(fasta_path) as f:
            sequence_lines = []
            for line in f:
                if not line.startswith(">"):
                    sequence_lines.append(line.strip())
            sequence = "".join(sequence_lines)

        json_data={
            "name":f"{name}",
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
        
        output_file = f"{output_dir}/{name}.json"

        # Write the json file 
        with open(output_file, "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"{name}.json created")