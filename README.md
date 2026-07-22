# Effector-Structure-Prediction
Pipeline for predicting effector structures. Using BioPython and mmCIF files. 

**Background**: 
I would like to use ESMFold, AF2 and AF3 to predict fungal effector structures. Effectors are secreted virulent proteins by pathogens that evoke an immune response in the host organism. They are structurally very diverse, and little is known on how to predict their structures from their amino sequence.

I already collected 80 fungal effector structures that are experimentally resolved and available in the PDB database. I based this on literature reviews and recent papers. 

Note on chain identifiers: author chain ID (auth_asym_id) and mmCIF (label_asym_id) exist. Since auth_asym_id is more often used, and also in literature, we use that chain.

The **input** for this project is simply:
- A .txt file called "PDB_ID_list.txt" with in one column, a list of all PDB ID's and its specific chain (based on auth_asym_id).

```
PDB_ID
1FN8.A
1KG1.A
1KPT.A
4GVB.B
```

And a .txt file called "PDB_ID_list.txt" with in one column all the protein identities.
```
PDB_ID
1FN8_1
1KG1_1
1KPT_1
4GVB_2
```

Note that the chains are PDB labelled by the protein identity, and not by the specific chain. It is assumed that all the chains within a protein identity is identical. 

1. From the .txt file, we want to download all the mmCIF files. On July 2027, the mmCIF file will be the standard, overruling the legacy .pdb files. We extract and read within the mmCIF using BioPython. We can get out the exact sequence (on which we will perform ESMFold, AlphaFold etc), and we can get out the crystal structure coordinates. Use this script to download the cif files:

```
python /home/rachel/cif/download_cif.py
```

2. Use the **extract_sequences.py** to create all the fasta files for each protein ID. 

```
python /home/rachel/cif/extract_sequences.py
```

4. For AF3, **run create_json_AF3.py**. This creates all json files for AF3. Once the json files are created, run **run_AF3_all.py** to run AF3 for all.
```
python /home/rachel/alphafold-models-3.0.3/create_json_AF3.py
bash /home/rachel/alphafold-models-3.0.3/run_AF3_all.sh
```

5. For ESMFold, we want to use the fasta files as well. 

```
bash /home/rachel/esmfold-1.0.3/run_all_esmfold2.sh
```

6. We want to also use TMAlign to compare the results. We downloaded the cif files, but we now need to extract only the right chains. 

```
python cif_single_chain.py
```

We then need to run TMAlign on AF3, and ESMFold. 

```
bash /home/rachel/TM-align/run_tmalign_batch.sh #for ESM
bash /home/rachel/TM-align/run_tmalign_batch2.sh #for AF3
```

7. We need to compile all the results in a tsv file.
```
python /home/rachel/TM-align/results/extract_tmalign_metadata2.py #for ESM
python /home/rachel/alphafold-models-3.0.3/extract_tmalign_metadata3.py
```






