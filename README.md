# Effector-Structure-Prediction
Pipeline for predicting effector structures. 

**Background**: 
I would like to use ESMFold, AF2 and AF3 to predict fungal effector three-dimensional structures. Plant pathogens can secrete effectors, which are virulent proteins that can manipulate plant immunity. They are structurally diverse, and little is known on how to accurately predict their structures from their amino sequence.

I collected 80 fungal effector structures that are experimentally resolved and available in the PDB database. I based this on literature reviews and recent papers. The metadata for this is under 

```
~/04_results_tsv/pdb_metadata.tsv
```

The first few rows look like:

| PDB_ID   | Chain   | Annotation                  | Organism                             | Deposition_date               | Structural family (inferred from La Naour Vernet et al. (2025))   |   How many protein identities in crystal structure | Method       |   Resolution |
|:---------|:--------|:----------------------------|:-------------------------------------|:------------------------------|:------------------------------------------------------------------|---------------------------------------------------:|:-------------|-------------:|
| 1FN8_1   | A       | TRYPSIN                     | Fusarium oxysporum (5507)            | 2000-08-21T00:00:00.000+00:00 | HYDROLASE/HYDROLASE SUBSTRATE (non secreted)                      |                                                  2 | 0            |         0.81 |
| 1KG1_1   | A       | Necrosis Inducing Protein 1 | Rhynchosporium secalis (38038)       | 2001-11-26T00:00:00.000+00:00 | /                                                                 |                                                  1 | Solution NMR |         0    |
| 1KPT_1   | A, B    | KP4 TOXIN                   | Ustilago maydis (5270)               | 1995-06-06T00:00:00.000+00:00 | KP4-like                                                          |                                                  1 | X-ray        |         1.75 |
| 1ZLD_1   | A       | Ptr necrosis toxin          | Pyrenophora tritici-repentis (45151) | 2005-05-06T00:00:00.000+00:00 | ToxA-like                                                         |                                                  1 | X-ray        |         1.65 |
| 1ZLE_1   | A, B, C | Ptr necrosis toxin          | Pyrenophora tritici-repentis (45151) | 2005-05-06T00:00:00.000+00:00 | ToxA-like                                                         |                                                  1 | X-ray        |         1.9  |

The PDB_ID contains the 4 letter code, and underscore of the protein entity. 1FN8_1 and 1FN8_2 belong to the same resolved crystal structure, but only the first entity is an effector. 

The chains in the metadate file show both the PDB labels (label_asym_id) and in square brackets the author chain ID's (auth_asym_id). Certain softwares use one or another, therefore it is important to collect information on both. 

There are two **inputs** for this project:
- The metadata file describe above. As long as the first column is included, it is possible to use a different metadata table, with different columns. I chose this information since we want to later cluster the results based on these characteristics specfically.
- A .txt file called "PDB_ID_list_chain.txt" with in one column, a list of all PDB ID's and its specific chain (based on auth_asym_id). We only consider one chain to be the effector. 

The text file is under
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

**Running**

To run the pipeline, first make sure you have all the requirements installed. It is recommended to use a virtual environment. 
```bash
pip install --upgrade pip
```

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r ~/requirements.txt
```

Then the pipeline is as follows:

```text
01_prepare_cif 
(run prepare_cif_main.py)
    |
02_folding
(run 'run_all_esm.sh')
(run af2, note: code not in this repository)
(run 'af3_main.py')
    |
03_tm_align
(run tm_align_esm.sh)
(run tm_align_af3.sh)
    |
04_results_tsv
(run main_tsv.py)
    |
05_graphs
(run graphs_tsv.ipynb)
    |
06_clustering
(run exp_clustering.sh)
(run esm_clustering.sh)
(run af3_clustering.sh)
(run umap.ipynb)
```

**Notes:**

The code for running AF2 is not documented in this repository. For AF2, the TM-align version 2024 was used (?), whereas for ESM and AF3, TM-align 2022 was used. Also, AF2 uses the experimentally resolved structures from .pdb files. It contains missing data for 4BJM_1, 8DP8_1, 8DP9_1. ESMFold and AF3 have complete datasets, and use the .cif files for the experimentally resolved structures. 

The current scripts use ESM and AF3 running on the same server, with each using 1 GPU. 