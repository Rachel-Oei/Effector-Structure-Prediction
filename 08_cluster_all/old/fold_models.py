import subprocess

class Fold:
    def __init__(
            self, pipeline, folding_method, proteins_per_cluster, gpu, json_dir, 
            processed_fasta_dir, processed_fasta_file):

        self.pipeline=pipeline
        self.folding_method=folding_method
        self.proteins_per_cluster=proteins_per_cluster
        self.gpu=gpu
        self.json_dir=json_dir
        self.processed_fasta_dir=processed_fasta_dir
        self.processed_fasta_file=processed_fasta_file
        self.input_fasta_dir=None
        self.cluster_dir=None
        self.cluster_basename=None
        self.protein_basename=None
        self.genome_basename=None
        self.output_dir=None

    def find_fastas_per_cluster(self):
        self.cluster_dir=f"/home/rachel/07_fold_all/{self.folding_method}/clusters"
        for fasta in self.cluster_dir:
            #extract the first {proteins_per_cluster} fasta files
            # add it to a folder with all fasta files ever extract 
            # put it in "/home/rachel/07_fold_all/{folding_method}/fasta"
            # if already {proteins_per_cluster} inside, then skip 

    def extract_names(self):
        self.input_fasta_dir=f"/home/rachel/08_cluster_all/{self.folding_method}/fasta"
        # self.cluster_basename="p_effector_100.fasta" #basename of ".fasta"
        # self.protein_basename=">GCA_016166325.FUN_012160-T1 FUN_012160" #everything after ">"
        # self.cluster_basename="Cluster_1126.fasta" #basename of ".fasta"
        # self.protein_basename=">multicluster_100-consensus" #everything after ">"
        self.genome_basename=self.protein_basename.split(".")

    def cut_signal_cleavage(self):
        # Use script I already have for moving the fasta files into a new folder called 
        # single_cut_fastas
        # Need to combine the FOEC and EffectorP pipeline

    def create_json_af3(self):
        # Already exists script
        # Think about how many directories I want the user to be able to specify.
        # But probably all of them, so that they can clearly see where everything is going          

    def run_af3(self):
        # First create json files 
        create_json_af3()

        subprocess.run(["bash", "run_af3.sh", str(self.gpu), str(self.processed_fasta_file)])

    def run_af2(self):
        subprocess.run(["bash", "run_af2.sh", str(self.gpu), str(self.processed_fasta_file)])

    def run_esm(self):
        subprocess.run(["bash", "run_esm.sh", str(self.gpu), str(self.processed_fasta_file)])

    def run (self):
        self.find_fastas_per_cluster()
        self.extract_names()
        self.cut_signal_cleavage()
    
        for protein in self.processed_fasta_dir:
            self.processed_fasta_file=protein
    
            if self.folding_method=="af3":
                self.run_af3()
    
            elif self.folding_method=="af2":
                self.run_af2()
    
            elif self.folding_method=="esm":
                self.run_esm() 
    
            else: 
                print("Could not find valid folding method")
                break #(Or continue?)

            # Script of folding method should only be for one protein, not for multiple 
            
    # output is in the tmp folder but also in your home directory. The home directory folders
    # are determined solely by the user input variables.
    # all of the code should be the same.
    # should have one code for af3, one of af2 and esm.

