from Bio.PDB.MMCIF2Dict import MMCIF2Dict

# Create a folder called cif_fasta
text_file="/home/rachel/cif/PDB_ID_list.txt"
input_directory="/home/rachel/cif/cif_downloads/"
output_directory="/home/rachel/cif/cif_fasta/"

"""
example dictionary output: 

dictionary["_entity_poly.pdbx_strand_id"]
# ['A', 'B']
dictionary["_entity_poly.pdbx_seq_one_letter_code_can"]
# ['IVGGTSASAGD...RSFIDTYA', 'GAR']
"""

def get_sequence_by_chain(cif_file, chain):
    d = MMCIF2Dict(cif_file)

    strand_ids = d["_entity_poly.pdbx_strand_id"]
    sequences = d["_entity_poly.pdbx_seq_one_letter_code_can"]

    for strand_id, sequence in zip(strand_ids, sequences):
        if chain in strand_id.split(","):
            return sequence.replace("\n", "")

with open("/home/rachel/cif/PDB_ID_list2.txt") as f:
    protein_ID_list = [line.strip() for line in f if line.strip()]

for protein_id in protein_ID_list:
    protein=protein_id[:4]
    chain=protein_id[5]
    cif_file=f"{input_directory}{protein}.cif"
    sequence = get_sequence_by_chain(cif_file, chain)
    output_file = f"{output_directory}{protein}.fasta"

    with open(output_file, "w") as f:
        f.write(f">{protein}\n")
        f.write(sequence + "\n")

    print(f"Created {output_file}")