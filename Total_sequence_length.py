import pandas as pd
import numpy as np

# --- Configuration Parameters ---
# Consider using English filenames if appropriate for your workflow
# input_filename = 'Gene_Presence_Absence_COG_Perfect.xlsx' 
# output_filename = 'Strain_COG_Total_Gene_Lengths.xlsx'
input_filename = 'present_absent.xlsx' # Original filename kept
output_filename = 'COG_length.xlsx' # Original filename kept

# Column indices (0-based)
gene_col_index = 0         # First column (Assumed Gene ID or similar)
gene_length_col_index = 5  # Sixth column (Gene length)
cog_col_index = 4          # Fifth column (COG category)
first_strain_col_index = 6 # Seventh column onwards (Strains)

# COG functional category list
cog_categories = ['J', 'K', 'L', 'C', 'E', 'F', 'G', 'H', 'I', 'P', 'Q', 'D', 'M', 'N', 'O', 'T', 'U', 'V']

# --- Read Excel File ---
try:
    # Assume the first row is the header (header=0)
    df = pd.read_excel(input_filename, header=0)
    print(f"Successfully read file: {input_filename}")
except FileNotFoundError:
    print(f"Error: File '{input_filename}' not found. Please ensure the file is in the script's directory or provide the full path.")
    exit()
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

# --- Data Preparation ---
# Get necessary column names (using index for robustness)
try:
    gene_length_col_name = df.columns[gene_length_col_index]
    cog_col_name = df.columns[cog_col_index]
    strain_names = df.columns[first_strain_col_index:].tolist()
    if not strain_names:
        print(f"Error: No strain columns found starting from column {first_strain_col_index + 1}. Please check the Excel file structure and 'first_strain_col_index' parameter.")
        exit()
    print(f"Found gene length column: '{gene_length_col_name}'")
    print(f"Found COG column: '{cog_col_name}'")
    print(f"Found {len(strain_names)} strain columns: {strain_names[0]} ... {strain_names[-1]}")
except IndexError:
    print("Error: Excel file has insufficient columns to find required columns based on provided indices. Please check the file and index parameters.")
    exit()

# 1. Convert gene length column to numeric type, setting non-convertible values to NaN
original_length_count = len(df)
df[gene_length_col_name] = pd.to_numeric(df[gene_length_col_name], errors='coerce')
# Check if any values became NaN after conversion (indicating non-numeric or empty original data)
nan_count = df[gene_length_col_name].isna().sum()
if nan_count > 0:
    print(f"Warning: Gene length column '{gene_length_col_name}' contains {nan_count} non-numeric or empty values. These genes will be treated as having length 0 in total length calculations.")
    # For summation, filling NaN with 0 is appropriate, although .sum() also treats NaN as 0 by default.
    # df[gene_length_col_name] = df[gene_length_col_name].fillna(0) # Or let .sum() handle it

# 2. Convert COG column to string type and treat NaN as empty strings
df[cog_col_name] = df[cog_col_name].astype(str).fillna('')

# --- Calculate Total Length ---
results = []

for strain in strain_names:
    # 1. Filter for genes present in this strain (corresponding column value is not blank/NaN)
    # Use .copy() to avoid SettingWithCopyWarning
    present_genes_df = df[pd.notna(df[strain])].copy() 

    # Using English column name for output consistency
    strain_total_lengths = {'Strain Name': strain} 

    if not present_genes_df.empty:
        # 2. For each COG category, calculate the total length of its genes in this strain
        for category in cog_categories:
            # Filter for genes belonging to this COG category (using .str.contains())
            # na=False ensures NaNs in the COG column don't cause errors and are treated as non-matches
            # regex=False for slight performance gain as we're matching literal characters
            category_genes = present_genes_df[
                present_genes_df[cog_col_name].str.contains(category, na=False, regex=False) 
            ]

            # Extract the lengths of these genes (already numeric, possibly including NaN)
            lengths = category_genes[gene_length_col_name]

            # Calculate the total length (pandas' sum() automatically treats NaN as 0)
            # If no genes belong to this category, the result will be 0
            total_length = lengths.sum() # Result is typically float or integer

            # Store the result in the dictionary, column name format "Category_TotalLen"
            strain_total_lengths[f'{category}_TotalLen'] = total_length

    else:
        # If the strain has no detected genes (based on non-empty values in its column)
        print(f"Warning: Strain '{strain}' has no detected genes (based on its column). All COG total lengths will be set to 0.")
        for category in cog_categories:
            strain_total_lengths[f'{category}_TotalLen'] = 0

    results.append(strain_total_lengths)

# --- Create and Save Output DataFrame ---
output_df = pd.DataFrame(results)

# Reorder columns to ensure 'Strain Name' is first, followed by COG category total lengths
output_columns = ['Strain Name'] + [f'{cat}_TotalLen' for cat in cog_categories]
output_df = output_df[output_columns]

try:
    # Total length is usually an integer, but could be float due to original data or NaN handling; 
    # pandas handles the type appropriately during saving.
    output_df.to_excel(output_filename, index=False)
    print(f"\nProcessing finished! Results saved to: {output_filename}")
except Exception as e:
    print(f"\nError saving results to Excel file: {e}")
