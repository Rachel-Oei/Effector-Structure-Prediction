# Effector-Structure-Prediction
Pipeline for predicting effector structures. Using BioPython and mmCIF files. 

**Background**: 
I would like to use ESMFold, AF2 and AF3 to predict fungal effector structures. Effectors are secreted virulent proteins by pathogens that evoke an immune response in the host organism. They are structurally very diverse, and little is known on how to predict their structures from their amino sequence.

I already collected 80 fungal effector structures that are experimentally resolved and available in the PDB database. I based this on literature reviews and recent papers. 

The **input** for this project is simply:
- A .txt file called "PDB_ID_list.txt" with in one column, a list of all PDB ID's and its specific chain.

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

1. From the .txt file, we want to download all the mmCIF files. On July 2027, the mmCIF file will be the standard, overruling the legacy .pdb files. We extract and read within the mmCIF using BioPython. We can get out the exact sequence (on which we will perform ESMFold, AlphaFold etc), and we can get out the crystal structure coordinates. Use the script **download_cif.py** to download the cif files. 

2. Use the **extract_sequences.py** to create all the fasta files for each protein ID. 

3. From the fasta files, you can run the ESMFold, AF2 and AF3. 

4. For AF3, **run create_json_AF3.py**. This creates all json files for AF3. Once the json files are created, run **run_AF3_all.py** to run AF3 for all.
```
python run_AF3_all.py
```

5. For ESMFold, we want to use the fasta files as well. 

```
bash /home/rachel/esmfold-1.0.3/run_all_esmfold.sh
```

6. TMAlign






