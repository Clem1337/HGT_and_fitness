import pandas as pd
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests

# Read data
data = pd.DataFrame({
    "Level": ["J", "K", "L", "C", "E", "F", "G", "H", "I", "P", "Q", "D", "M", "N", "O", "T", "U", "V"],
    "Species": [77, 272, 404, 180, 258, 81, 297, 95, 44, 173, 28, 100, 388, 41, 35, 72, 75, 109],
    "Genus": [44, 330, 1846, 182, 324, 79, 402, 151, 49, 351, 45, 98, 428, 11, 50, 67, 78, 152],
    "Family": [115, 176, 245, 72, 133, 120, 222, 83, 40, 121, 24, 41, 161, 0, 45, 24, 64, 104],
    "Order": [25, 170, 92, 38, 83, 46, 117, 40, 20, 74, 26, 48, 96, 7, 23, 28, 73, 49],
    "Class": [6, 129, 67, 10, 54, 21, 89, 22, 24, 32, 33, 1, 83, 0, 16, 9, 11, 52],
    "Phylum": [10, 110, 123, 32, 54, 34, 98, 30, 43, 64, 40, 7, 165, 4, 8, 20, 18, 57],
    "Total": [277, 1187, 2777, 514, 906, 381, 1225, 421, 220, 815, 196, 295, 1321, 63, 177, 220, 319, 523]
})

# Perform Fisher's Exact Test
enrichment_results = []
for level in ["Species", "Genus", "Family", "Order", "Class", "Phylum"]:
    for i, row in data.iterrows():
        table = [[row[level], row["Total"] - row[level]],
                 [data[level].sum() - row[level], data["Total"].sum() - data[level].sum()]]
        oddsratio, p_value = stats.fisher_exact(table)
        enrichment_results.append([row["Level"], level, p_value])

# Adjust P-values (FDR correction)
enrichment_df = pd.DataFrame(enrichment_results, columns=["Level", "Taxonomic Level", "P-value"])
enrichment_df["FDR"] = multipletests(enrichment_df["P-value"], method='fdr_bh')[1]

# Output results
enrichment_file_path = "Enrichment_Analysis_Results.csv"
enrichment_df.to_csv(enrichment_file_path, index=False)
print(f"Results saved to {enrichment_file_path}")
