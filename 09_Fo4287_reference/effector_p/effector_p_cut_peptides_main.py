import os 
from effector_p_cut_peptides_models import write_single_fastas

def main():

    signal_p_file="/home/rachel/09_Fo4287_reference/effector_p/output.gff3" 
    multi_fasta_file="/home/rachel/09_Fo4287_reference/effector_p/Fusarium_graminearum.proteins.fa" 
    output_fasta_dir="/home/rachel/09_Fo4287_reference/effector_p/single_cut_fasta" 

    os.makedirs(output_fasta_dir, exist_ok=True)

    write_single_fastas(multi_fasta_file, signal_p_file, output_fasta_dir)

if __name__ == "__main__":
    main()