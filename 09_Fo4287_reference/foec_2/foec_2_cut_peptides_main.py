import os 
from foec_2_cut_peptides_models import run_signal_p, move_fastas

def main():

    project_dir="/home/rachel/09_Fo4287_reference/foec_2"
    model_dir = "/home/rachel/07_fold_all/signalp6_slow_sequential/signalp-6-package/models"
    fasta_file=f"{project_dir}/GCA_003315725.1_08_putative_effectors_protein.fasta"
    signal_p_output=f"{project_dir}/signal_p_output"
    single_cut_fasta_out=f"{project_dir}/single_cut_fasta"

    os.makedirs(signal_p_output, exist_ok=True)
    os.makedirs(single_cut_fasta_out, exist_ok=True)

    run_signal_p(model_dir, fasta_file, signal_p_output)
    move_fastas(fasta_file, signal_p_output, single_cut_fasta_out)

if __name__ == "__main__":
    main()

    