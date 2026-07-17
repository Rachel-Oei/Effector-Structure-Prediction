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

Note that the chains are PDB labelled chains (label_asym_id), **not** the author labelled (auth_asym_id). 

1. From the .txt file, we want to download all the mmCIF files. On July 2027, the mmCIF file will be the standard, overruling the legacy .pdb files. We extract and read within the mmCIF using BioPython. We can get out the exact sequence (on which we will perform ESMFold, AlphaFold etc), and we can get out the crystal structure coordinates. Use the script ...






