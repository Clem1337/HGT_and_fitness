import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Read phenotypic data
file_path = "Phenotypic_Results.csv"  # Please ensure this file is in the current directory
data = pd.read_csv(file_path, index_col=0)  # Read data, the first column is strain ID

# Calculate Manhattan distance matrix
distance_matrix = squareform(pdist(data, metric="cityblock"))  # "cityblock" calculates Manhattan distance

# Convert to DataFrame
distance_df = pd.DataFrame(distance_matrix, index=data.index, columns=data.index)

# Save as CSV file
distance_df.to_csv("Phenotypic_Manhattan_Distance_Matrix.csv")

print("Phenotypic Manhattan distance matrix has been saved as 'Phenotypic_Manhattan_Distance_Matrix.csv'")
