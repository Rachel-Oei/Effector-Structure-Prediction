import requests 
import os
import gemmi
from typing import List
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

cif_directory = "/home/rachel/01_prepare_cif"

    input_text_chain = cif_directory + "/input_pdb_lists/pdb_list_chain.txt"
    input_text_entity = cif_directory + "/input_pdb_lists/pdb_list_entity.txt"

    cif_fasta_directory = cif_directory + "/cif_fasta/"
    cif_download_directory = cif_directory + "/cif_downloads/"
    cif_single_chain_directory = cif_directory + "/cif_single_chain/"

    create_directory(cif_download_directory)
    create_directory(cif_fasta_directory)
    create_directory(cif_single_chain_directory)

    download_cif(input_text_chain, cif_download_directory)
    map_chain_to_entity(input_text_chain, cif_download_directory, input_text_entity)
    extract_chain_sequences(input_text_entity, cif_download_directory, cif_fasta_directory)
    cif_single_chain(
        input_text_chain, 
        input_text_entity, 
        cif_download_directory, 
        cif_single_chain_directory
        )

def prepare_cif (input_text, fasta_dir, download_dir, output_dir):
    ######

def create_directory (nested_directory: str):
    """
    Creates directory if it not already exists
    """
    os.makedirs(nested_directory, exist_ok=True)
    
class Protein:
    def __init__(self, pdb_id, chain, entity=None, amino_acid_sequence=None):
        self.pdb_id=pdb_id
        self.chain=chain
        self.entity=entity
        self.amino_acid_sequence=amino_acid_sequence

class ProteinListController:
    def __init__(self, input_text):
        self.input_text=input_text
        self.protein_list=[]

    def generate_input_list (self: str) -> List[str] : 
        """
        Converts PDB codes from a .txt separated by new-lines into a list
        Input: .txt file delimited by new-lines.
            Example: 
            1FN8.A
            1KG1.A
            1KPT.A
            4GVB.B
        Return: [1FN8.A, 1KG1.A, 1KPT.A, 4GVB.B]
        """
        with open(self.input_text, "r") as f:
            for line in f:

                line = line.strip()
                
                pdb_id, chain = line.split(".")
                protein=Protein(pdb_id, chain)

                # Creates protein:
                # pdb_id = "1FN8"
                # chain = "A"
                # entity = None
                # amino_acid_sequence = None

                self.protein_list.append(protein)
        return self.protein_list

class ProteinController: 
    def __init__(self):

    def download_cif (self, protein, output_directory):
        """
        Downloads cif files from RCSB, from PDB codes in the input list
        Output file name e.g: 1FN8.cif
        """
        url = f"https://files.rcsb.org/download/{protein.pdb_id}.cif"
        output_final_directory=output_directory+f"{protein.pdb_id}.cif"
        response = requests.get(url, timeout=30)

        with open(output_final_directory, "wb") as out_file:
            out_file.write(response.content)

        print(f"Downloaded {protein.pdb_id}")

    def add_entity (self, protein, cif_directory):
        """
        """
        protein_directory=f"{cif_directory}{protein.pdb_id}.cif"

        d = MMCIF2Dict(protein_directory)
        entity_per_atom = d["_atom_site.label_entity_id"]
        chain_per_atom = d["_atom_site.auth_asym_id"]
        
        protein_chain=protein.chain
        entity_id=None
        for cif_entity, cif_chain in zip(entity_per_atom, chain_per_atom):
            if protein_chain == cif_chain:
                entity_id=cif_entity
                break

        if entity_id is None:
            raise ValueError(
                f"Could not find chain {protein.chain} "
                f"in {protein.pdb_id}"
            )

        protein.entity=entity_id

def main():
    # Generate the input list of proteins with information 
    protein_list_controller=ProteinListController.generate_input_list(
        "/home/rachel/01_prepare_cif/input_pdb_lists/pdb_list_chain.txt")

    protein_list=protein_list_controller.
    # Loop over each protein in the list, and perform the different steps:
    for protein in ProteinListController.protein_list: 
        ProteinController.download_cif(protein, "/home/rachel/cif/cif_downloads/")
        ProteinController.add_entity(protein, "/home/rachel/cif/cif_downloads/")


        ProteinController.extract_chain_sequence(protein)
        ProteinController.extract_single_chain_cif(protein)

def extract_chain_sequences(input_text, cif_directory, cif_fasta_directory):
    """
    Obtain fasta sequences from only the single chains that are used.
    """
    input_list=pdb_text_to_list(input_text)
    for protein_full in input_list:
        protein_id=protein_full[:4]
        entity_id=protein_full[5]
        protein_directory=f"{cif_directory}{protein_id}.cif"
        d = MMCIF2Dict(protein_directory)
        strand_ids = d["_entity_poly.entity_id"]
        sequences = d["_entity_poly.pdbx_seq_one_letter_code_can"]

        chain_sequence=None
        for strand_id, sequence in zip(strand_ids, sequences):
            if entity_id == strand_id:
                chain_sequence=sequence.replace("\n", "")
                break

        if chain_sequence is None:
            print(f"Could not find sequence {protein_full}")
            continue 

        output_file = f"{cif_fasta_directory}{protein_full}.fasta"

        with open(output_file, "w") as f:
            f.write(f">{protein_full}\n")
            f.write(chain_sequence + "\n")

        print(f"Created {output_file}")

def cif_single_chain (input_text_chain, 
                      input_text_entity, 
                      cif_download_directory, 
                      cif_single_chain_directory
                      ):
    """
    Removes irrelevant chains from cif file.
    """
    chain_list = pdb_text_to_list(input_text_chain)
    entity_list = pdb_text_to_list(input_text_entity)

    for id_with_chain, id_with_entity in zip (chain_list, entity_list):
        full_protein_id=id_with_entity[:6]
        protein_id=id_with_chain[:4]
        protein_chain=id_with_chain[5]

        cif_file=f"{cif_download_directory}{protein_id}.cif"
        structure = gemmi.read_structure(cif_file)

        if len(structure)>1:
            del structure[1:]

        found_chain = False
        for model in structure:
            chains_to_remove=[]
    
            for chain in model:
                print("name:", chain.name)
                print("id:", protein_chain)
    
                if chain.name != protein_chain:
                    chains_to_remove.append(chain.name)
                else:
                    found_chain = True
    
            for chain_name in chains_to_remove:
                model.remove_chain(chain_name)
    
        if not found_chain:
            print(f"WARNING: Chain {protein_chain} not found in {protein_id}")
            continue
    
        # Write single-chain mmCIF
        output_file = f"{cif_single_chain_directory}{full_protein_id}.cif"

        structure.make_mmcif_document().write_file(output_file)
    
        print(f"Created {output_file}")
