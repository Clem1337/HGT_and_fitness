from ete3 import Tree
import pandas as pd

# Read phylogenetic tree file
tree_file = "PAN_PHYLOGENY_MOD.nwk"  # Please ensure this file is in the current directory
tree = Tree(tree_file, format=1)

# Get all leaf node names (strain names)
leaf_names = [leaf.name for leaf in tree]

# Calculate genetic distance between all strains
distance_matrix = pd.DataFrame(index=leaf_names, columns=leaf_names)

for i in leaf_names:
    for j in leaf_names:
        if i == j:
            distance_matrix.loc[i, j] = 0  # Distance to itself is 0
        else:
            distance_matrix.loc[i, j] = tree.get_distance(i, j)

# Save as CSV file
distance_matrix.to_csv("Genetic_Distance_Matrix.csv")

print("Genetic distance matrix has been saved as 'Genetic_Distance_Matrix.csv'")
