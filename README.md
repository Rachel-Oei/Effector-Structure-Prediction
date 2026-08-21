# Effector-Structure-Prediction
*(Work-in-progress. Expected completion: 31 Aug 2026).*

Pipeline for predicting effector structures. 
    
- Part 1: folding 80 established effector structures (all have been experimentally resolved). Used as baseline results. 
- Part 2: folding effectors from hundreds of genomes. Whole genomes have been sequenced, and possible effectors have been annotated and clustered based on sequence similarity. Want to see whether structural similarity results in different clustering. Two pipelines have been developed: called 'Foec2' and 'EffectorP' pipelines throughout. This work builds on top of existing work. 

**Background**: 
Plant pathogens can secrete effectors, which are virulent proteins that can manipulate plant immunity. They are structurally diverse, and little is known on how to accurately predict their structures from their amino sequence.

**Part 1:**
I collected 80 fungal effector structures that are experimentally resolved and available in the PDB database. I based this on literature reviews and recent papers. The metadata for this is under:

```
~/04_results_tsv/pdb_metadata.tsv
```

The first few rows look like:
| PDB_ID   | Chain   | Annotation                  | Organism                             | Deposition_date               | Structural family (inferred from La Naour Vernet et al. (2025))   |   How many protein identities in crystal structure | Method       |   Resolution |
|:---------|:--------|:----------------------------|:-------------------------------------|:------------------------------|:------------------------------------------------------------------|---------------------------------------------------:|:-------------|-------------:|
| 1FN8_1   | A       | TRYPSIN                     | Fusarium oxysporum (5507)            | 2000-08-21 | HYDROLASE/HYDROLASE SUBSTRATE (non secreted)                      |                                                  2 | 0            |         0.81 |
| 1KG1_1   | A       | Necrosis Inducing Protein 1 | Rhynchosporium secalis (38038)       | 2001-11-26 | /                                                                 |                                                  1 | Solution NMR |         0    |
| 1KPT_1   | A, B    | KP4 TOXIN                   | Ustilago maydis (5270)               | 1995-06-06 | KP4-like                                                          |                                                  1 | X-ray        |         1.75 |
| 1ZLD_1   | A       | Ptr necrosis toxin          | Pyrenophora tritici-repentis (45151) | 2005-05-06 | ToxA-like                                                         |                                                  1 | X-ray        |         1.65 |
| 1ZLE_1   | A, B, C | Ptr necrosis toxin          | Pyrenophora tritici-repentis (45151) | 2005-05-06 | ToxA-like                                                         |                                                  1 | X-ray        |         1.9  |

The PDB_ID contains the 4 letter code, and underscore of the protein entity, i.e 1FN8_1 and 1FN8_2 belong to the same resolved crystal structure, but only the first entity is an effector. 

The chains in the metadate file show both the PDB labels (label_asym_id) and in square brackets the author chain ID's (auth_asym_id). Certain softwares use one or another, therefore it is important to collect information on both. 

There are two **inputs** for this part of the project:
- The metadata file describe above. As long as the first column is included, it is possible to use a different metadata table, with different columns. I chose this information since we want to later cluster the results based on these characteristics specfically.
- A .txt file called "PDB_ID_list_chain.txt" with in one column, a list of all PDB ID's and its specific chain (based on auth_asym_id). We only consider one chain to be the effector. 

The latter is under:
```
~/01_prepare_cif/input_pdb_lists/PDB_ID_list_chain.txt
```

It looks like: 

```
1FN8.A
1KG1.A
1KPT.A
4GVB.B
```

Again, the chains are according to auth_asym_id. 

To run the pipeline, first make sure you have all the requirements installed. It is recommended to use a virtual environment. I use venv for this.

```bash
pip install --upgrade pip
python3 -m venv venv
source venv/bin/activate
pip install -r ~/requirements.txt
```

**ESMFold**


**AlphaFold2**


**AlphaFold3**


**TM-Align**

Then the pipeline is as follows:

```text
01_prepare_cif 
(python prepare_cif_main.py)
    |
02_folding
(bash 'run_all_esm.sh')
(bash 'run_all_af2.sh')
(python 'af3_main.py')
    |
03_tm_align
(bash tm_align_esm.sh)
(bash tm_align_af2.sh)
(bash tm_align_af3.sh)
    |
04_results_tsv
(python main_tsv.py)
    |
05_graphs
(I ran graphs_tsv.ipynb in GitHub codespaces, execution found in this repo)
    |
06_clustering
(bash exp_clustering.sh)
(bash esm_clustering.sh)
(bash af2_clustering.sh)
(bash af3_clustering.sh)
(I ran umap.ipynb in GitHub codespaces, execution found in this repo)
```

**Notes:**

The current scripts use ESM, AF2, AF3 running on the same server, with each using 1 GPU. 

Next: 
AF3 look at how many homologs it found in the database. Color the graphs by that. runtime and the tm score.


```bash 
#!/bin/bash

# Download version 6 through https://services.healthtech.dtu.dk/services/SignalP-6.0/

# tar -xzf signalp-6.0i.slow_sequential.tar.gz
# pip install -r requirements.txt
# pip install signalp6_slow_sequential/signalp-6-package/
# pip install "numpy<2"

## Because signal p only operates with python 3.10, and I had 3.12, 
## I had to activate a conda environmnet with version 3.9

# Download miniconda to get conda inside the server:
# cd ~
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# bash Miniconda3-latest-Linux-x86_64.sh

# export PATH="$HOME/miniconda3/bin:$PATH"
# conda create -n signalp310 python=3.9

## To activate everytime:
# export PATH="$HOME/miniconda3/bin:$PATH" 
# source "$HOME/miniconda3/bin/activate" signalp39

## Installing the signal-p package 
# cd ~/07_fold_all/signalp6_slow_sequential/signalp-6-package
# python -m pip install .

# Fungi are eukaryotic organisms, short output with no graphics, slow prediction mode. 

signalp6 \
    --model_dir "/home/rachel/07_fold_all/signalp6_slow_sequential/signalp-6-package/models/" \
    --ff $all_aa_dir \
    --org eukarya \
    --od $out_dir \
    --fmt txt \
    --mode slow-sequential
```