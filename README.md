# Effector-Structure-Prediction
*(Work-in-progress. Expected completion: 31 Aug 2026).*

Pipeline for predicting effector structures. 

**Background**: 
Plant pathogens can secrete effectors, which are virulent proteins that can manipulate plant immunity. They are structurally diverse, and little is known on how to accurately predict their structures from their amino sequence.

**Part 1:**
I first fold 80 established effector structures (all have been experimentally resolved, in PDB). Used this as the baseline for my results. The selection was made based on literature reviews and recent papers. The metadata for this is under:

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

**Notes:**
The current scripts use ESM, AF2, AF3 running on the same server, with each using 1 GPU. 

**TM-Align**
```bash
# Requires an activated Python venv

# Download
wget https://zhanggroup.org/TM-align/TMalign.cpp

# Compile
g++ -O3 -ffast-math -lm -o TMalign TMalign.cpp
```

**FoldSeek**
```bash
# Requires an activated Python venv

# Download and extract
wget https://mmseqs.com/foldseek/foldseek-linux-gpu.tar.gz
tar xvzf foldseek-linux-gpu.tar.gz
```

Then the pipeline is as follows:

```text
01_prepare_cif 
(python prepare_cif_main.py)
    |
02_folding
(bash 'run_all_esm.sh')
(bash 'run_all_af2.sh')
(bash 'run_all_af3.sh')
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

**Part 2**
Folding effectors from hundreds of genomes. Whole genomes have been sequenced, and possible effectors have been annotated and clustered based on sequence similarity. Want to see whether structural similarity results in different clustering. Two pipelines have been developed: called 'Foec2' and 'EffectorP' pipelines throughout. This work builds on top of existing work. 

**SignalP**
```bash 
# SignalP 6.0 installation. Note: It only works with versions of Python 3.10 or lower.
# Download inside ~/07_fold_all from: https://services.healthtech.dtu.dk/services/SignalP-6.0/

# Extract package
tar -xzf signalp-6.0i.slow_sequential.tar.gz

# Install Miniconda
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
export PATH="$HOME/miniconda3/bin:$PATH"

# Create and activate environment
conda create -n signalp39 python=3.9
source "$HOME/miniconda3/bin/activate" signalp39

# Install SignalP
cd ~/07_fold_all/signalp6_slow_sequential/signalp-6-package
pip install -r requirements.txt
pip install "numpy<2"
python -m pip install .
```

Then the pipeline is as follows:
```text
07_fold_all
(python foec_2_signal_p_main.py)
(python effector_p_signal_p_main.py)
    |
08_cluster_all
```

**Notes:**
The current scripts use ESM, AF2, AF3 running on the same server, with each using 1 GPU. 

Next: 
AF3 look at how many homologs it found in the database. Color the graphs by that. runtime and the tm score.