# Effector-Structure-Prediction
Pipeline for predicting effector structures. 

**Background**: 
I would like to use ESMFold, AF2 and AF3 to predict fungal effector structures. Effectors are secreted virulent proteins by pathogens that evoke an immune response in the host organism. They are structurally very diverse, and little is known on how to predict their structures from their amino sequence.

I already collected 80 fungal effector structures that are experimentally resolved and available in the PDB database. I based this on literature reviews and recent papers. 

The **input** for this project is simply:
- A .txt file with PDB ID's (single column and delimited by newlines).

Notes on the **PDB ID's**:
- It is possible that a PDB ID contains multiple protein ID's (for instance, one effector and one receptor that were experimentally resolved together). For instance, 6FUB can be divided into 6FUB_1 and 6FUB_2. We choose the protein ID that contains the effector, so 6FUB_2 in this case.
- Each protein ID can also contain multiple chains. 6FUB_2 can contain chain A, B, C etc. We assume that all the chains within a protein ID are identical. Therefore, we choose the first chain that is mentioned, such as chain A. 
- Sometimes, there is a difference between the PDB chain label, and the label by the author. For e.g: chain A[B auth], means that the PDB considers the chain to be A, but the author originally deposited it as B. In this case, we choose the chain to be B, because that is what is in the .pdb file. 

1. Creation of effector table.
