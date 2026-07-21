import os 
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

# Create a folder called cif_fasta
text_file="/home/rachel/cif/PDB_ID_list2.txt"
input_directory="/home/rachel/cif/cif_downloads/"
output_directory="/home/rachel/cif/cif_fasta/"

"""
MMCIF2Dict dictionary looks like: 
d["_struct_asym.id"]         = ["A", "B"]
d["_struct_asym.entity_id"]  = ["1", "1"]
d["_entity_poly.entity_id"]  = ["1"]
d["_entity_poly.pdbx_seq_one_letter_code_can"] = ["MKVLAT...GYQG"]

"""
for filename in os.listdir(input_directory):
    protein_id=filename[:4] # to remove .cif extension
    cif_path=input_directory+f"{protein_id}.cif"

    dictionary=MMCIF2Dict(cif_path)

    entity_to_seq = dict(zip(
        dictionary["_entity_poly.entity_id"],
        dictionary["_entity_poly.pdbx_seq_one_letter_code_can"]
    ))

    seq = entity_to_seq.get(str(entity_id))
    return seq.replace("\n", "") if seq else None

