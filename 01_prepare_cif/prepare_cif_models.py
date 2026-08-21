import requests 
import gemmi
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import json

class Protein:
    """
    Each protein has a pdb_id, chain, identity and amino acid sequence. 
    Therefore we use a class to store their attributes. 

    protein = Protein("1FN8", "A") gives:

    protein.pdb_id              -> "1FN8"
    protein.chain               -> "A"
    protein.entity              -> None
    protein.amino_acid_sequence -> None
    """
    def __init__(self, pdb_id, chain, entity=None, amino_acid_sequence=None):
        self.pdb_id=pdb_id
        self.chain=chain
        self.entity=entity
        self.amino_acid_sequence=amino_acid_sequence

    def download_cif (self, output_directory):
        """
        Downloads cif files from RCSB, from PDB codes in the input list
        Output file name e.g: 1FN8.cif
        """
        url = f"https://files.rcsb.org/download/{self.pdb_id}.cif"
        output_final_directory=output_directory+f"{self.pdb_id}.cif"
        response = requests.get(url, timeout=30)

        with open(output_final_directory, "wb") as f:
            f.write(response.content)

        print(f"Downloaded {self.pdb_id}")

    def map_entity (self, cif_download_directory):
        """
        Finds the entity from the chain (auth_asym_id) using the MMCIF2Dict.
        """
        protein_directory=f"{cif_download_directory}{self.pdb_id}.cif"
        
        d = MMCIF2Dict(protein_directory)
        entity_per_atom = d["_atom_site.label_entity_id"]
        chain_per_atom = d["_atom_site.auth_asym_id"]
        
        protein_chain=self.chain
        entity_id=None
        for cif_entity, cif_chain in zip(entity_per_atom, chain_per_atom):
            if protein_chain == cif_chain:
                entity_id=cif_entity
                break

        if entity_id is None:
            raise ValueError(
                f"Could not find chain {self.chain} "
                f"in {self.pdb_id}"
            )

        self.entity=entity_id
        return self.entity

    def extract_chain_sequence(self, cif_download_directory, cif_fasta_directory):
        """
        Obtain fasta sequences from only the single chains that are used.
        Store them in a new directory and in the Protein class. 
        """    
        protein_directory=f"{cif_download_directory}{self.pdb_id}.cif"
        d = MMCIF2Dict(protein_directory)
        strand_ids = d["_entity_poly.entity_id"]
        sequences = d["_entity_poly.pdbx_seq_one_letter_code_can"]

        chain_sequence=None
        for strand_id, sequence in zip(strand_ids, sequences):
            if self.entity == strand_id:
                chain_sequence=sequence.replace("\n", "")
                break

        if chain_sequence is None:
            print(f"Could not find sequence {self.pdb_id}_{self.entity}")
            return None  

        self.amino_acid_sequence=chain_sequence
        output_file = f"{cif_fasta_directory}{self.pdb_id}_{self.entity}.fasta"

        with open(output_file, "w") as f:
            f.write(f">{self.pdb_id}_{self.entity}\n")
            f.write(self.amino_acid_sequence + "\n")

        print(f"Created {output_file}")

        return self.amino_acid_sequence

    def cif_single_chain (self, cif_download_directory, cif_single_chain_directory
                      ):
        """
        Cif file contains 3D structural information. 
        This function removes irrelevant chains from cif file.
        """
        cif_file=f"{cif_download_directory}{self.pdb_id}.cif"
        structure = gemmi.read_structure(cif_file)

        if len(structure)>1:
            del structure[1:]

        found_chain = False
        for model in structure:
            chains_to_remove=[]
    
            for chain in model:
                if chain.name != self.chain:
                    chains_to_remove.append(chain.name)
                else:
                    found_chain = True
    
            for chain_name in chains_to_remove:
                model.remove_chain(chain_name)
    
        if not found_chain:
            print(f"WARNING: Chain {self.chain} not found in {self.pdb_id}")
            return 
    
        # Write single-chain mmCIF
        output_file = f"{cif_single_chain_directory}{self.pdb_id}_{self.entity}.cif"

        structure.make_mmcif_document().write_file(output_file)
    
        print(f"Created {output_file}")

    def create_json (self, output_dir):
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
        if self.amino_acid_sequence is None:
            print(
                f"WARNING: No sequence available for "
                f"{self.pdb_id}_{self.entity}. JSON not created."
            )
            return
        
        json_data={
            "name":f"{self.pdb_id}_{self.entity}",
            "sequences": [
            {
                "protein": {
                "id": [self.chain],
                "sequence": self.amino_acid_sequence
                }
            }
            ],
            "modelSeeds": [1],
            "dialect": "alphafold3",
            "version": 1
        }
        
        output_file = f"{output_dir}/{self.pdb_id}_{self.entity}.json"

        # Write the json file 
        with open(output_file, "w") as f:
            json.dump(json_data, f, indent=2)

        print(f"{output_file} created")
    
class AllProteins:
    """
    This class loops over all the proteins. 
    ├── Protein 1
    │     ├── pdb_id = 1FN8
    │     ├── chain = A
    │     ├── entity = ...
    │     └── amino_acid_sequence = ...
    │
    ├── Protein 2
    │     ├── pdb_id = 1KG1
    │     ├── chain = A
    │     ├── entity = ...
    │     └── amino_acid_sequence = ...
    """
    def __init__(self, input_text):
        self.input_text=input_text
        self.protein_list=[]
        self.generate_input_list()

    def generate_input_list (self) : 
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

                line = line.strip() # Removes any leading and trailing whitespaces 
                
                pdb_id, chain = line.split(".")
                protein=Protein(pdb_id, chain) # Updates the Protein class 

                # Creates protein:
                # pdb_id = "1FN8"
                # chain = "A"
                # entity = None
                # amino_acid_sequence = None

                self.protein_list.append(protein) # Adds the protein to the total protein list 

        return self.protein_list

    def download_all (self, cif_download_directory):
        for protein in self.protein_list:
            protein.download_cif(cif_download_directory)

    def map_entities (self, cif_download_directory):
        for protein in self.protein_list:
            protein.map_entity(cif_download_directory)

    def extract_chain_sequences(self, cif_download_directory, cif_fasta_directory):
        for protein in self.protein_list:
            protein.extract_chain_sequence(cif_download_directory, cif_fasta_directory)

    def cif_single_chain_all(self, cif_download_directory, cif_single_chain_directory):
        for protein in self.protein_list:
            protein.cif_single_chain(cif_download_directory, cif_single_chain_directory)

    def create_json_all(self, output_dir):
        for protein in self.protein_list:
            protein.create_json(output_dir)