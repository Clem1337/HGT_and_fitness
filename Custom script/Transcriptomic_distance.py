import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon
from itertools import combinations

# Read data
file_path = "Single_Culture_tpm.xlsx"
df = pd.read_excel(file_path)

# Extract bacteria columns
bacteria_cols = df.columns[3:]

# Process COG categories
cog_exp = {}
for _, row in df.iterrows():
    gene = row["Gene"]
    cogs = str(row["COG_category"])  # Ensure it is a string
    if cogs in ["nan", "None", ""] or pd.isna(cogs):
        continue  # Skip genes without COG annotation

    cogs = list(cogs)  # Parse COG categories, e.g., "KL" → ["K", "L"]
    tpm_values = row[bacteria_cols]  # Get expression values of this gene in each bacteria

    if tpm_values.isna().all():
        continue  # Skip if no bacteria have this gene

    for cog in cogs:
        if cog not in cog_exp:
            cog_exp[cog] = {bac: np.nan for bac in bacteria_cols}  # Initialize as NaN
        for bac in bacteria_cols:
            cog_exp[cog][bac] = tpm_values[bac] / len(cogs) if not pd.isna(tpm_values[bac]) else np.nan

# Build COG expression matrix
cog_df = pd.DataFrame.from_dict(cog_exp, orient="index")

# Calculate Jensen-Shannon Divergence, using only **common genes**
bacteria_pairs = list(combinations(bacteria_cols, 2))
jsd_results = []

for bac1, bac2 in bacteria_pairs:
    common_genes = cog_df[[bac1, bac2]].dropna()  # Keep only genes that are **not empty** for both bacteria
    if common_genes.empty:
        jsd = np.nan  # Return NaN if no common genes
    else:
        p = common_genes[bac1].values
        q = common_genes[bac2].values
        jsd = jensenshannon(p, q, base=2)  # Calculate JSD

    jsd_results.append([bac1, bac2, jsd])

# Save results
output_df = pd.DataFrame(jsd_results, columns=["Bacteria1", "Bacteria2", "JSD_distance"])
output_df.to_csv("Bacteria_Expression_Distance_Shared_Genes.csv", index=False)

print("Calculation completed, JSD calculated based on common genes only, results saved to 'Bacteria_Expression_Distance_Common_Genes.csv'")
