import pandas as pd
from scipy import stats

def find_cutoff(df, target_col='distantly', r_col='r', p_threshold=0.05):
    """
    Finds the cut-off and the direction of the r difference.

    Args:
        df (pd.DataFrame): Input DataFrame.
        target_col (str): Name of the target column.
        r_col (str): Name of the r column.
        p_threshold (float): P-value threshold.

    Returns:
        tuple: (cut_off, p_value, r_direction) or (None, None, None).
               r_direction:  1 if r is higher above the cut-off,
                            -1 if r is lower above the cut-off,
                            None if no significant cut-off.
    """

    df_sorted = df.sort_values(target_col)
    best_cutoff = None
    best_p_value = 1.0
    best_r_direction = None  # Store the direction

    for i in range(1, len(df_sorted) - 1):
        cutoff_value = df_sorted[target_col].iloc[i]
        group1 = df_sorted[df_sorted[target_col] < cutoff_value]
        group2 = df_sorted[df_sorted[target_col] >= cutoff_value]

        if len(group1) >= 2 and len(group2) >= 2:
            t_stat, p_value = stats.ttest_ind(group1[r_col], group2[r_col], equal_var=False)

            if p_value < best_p_value:
                best_p_value = p_value
                best_cutoff = cutoff_value

                # Calculate the means and determine the direction
                mean_group1 = group1[r_col].mean()
                mean_group2 = group2[r_col].mean()
                best_r_direction = 1 if mean_group2 > mean_group1 else -1


    if best_p_value < p_threshold:
        return best_cutoff, best_p_value, best_r_direction
    else:
        return None, None, None

def analyze_single_sheet(excel_file, sheet_name, categories=['closely', 'intermediate', 'distantly'], r_col='r', p_threshold=0.05):
    """
    Analyzes a single sheet in an Excel file, finding cut-offs and r direction.

    Args:
        excel_file (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to analyze.
        categories (list): List of category column names.
        r_col (str): Name of r column.
        p_threshold (float): P-value threshold.

    Returns:
        pd.DataFrame: Results for each category in the single sheet.
    """

    results_list = []
    df = pd.read_excel(excel_file, sheet_name=sheet_name) # Directly read the specified sheet
    print(f"Processing sheet: {sheet_name}")


    for category in categories:
        if category not in df.columns or r_col not in df.columns:
            print(f"  Error: '{category}' or '{r_col}' column not found in {sheet_name}.")
            results_list.append({
                'Sheet Name': sheet_name,
                'Category': category,
                'Cut-off': None,
                'P-value': None,
                'R Direction': None  # Add R Direction to the results
            })
            continue

        cutoff, p_value, r_direction = find_cutoff(df, category, r_col, p_threshold)

        if cutoff is not None:
            print(f"  Category '{category}': Found cut-off: {cutoff:.4f} (p={p_value:.4f}), R Direction: {'Higher' if r_direction == 1 else 'Lower'}")
        else:
            print(f"  Category '{category}': No significant cut-off found.")

        results_list.append({
            'Sheet Name': sheet_name,
            'Category': category,
            'Cut-off': cutoff,
            'P-value': p_value,
            'R Direction': r_direction  # Add R Direction to the results
        })

    return pd.DataFrame(results_list)

# Example usage for a single sheet
excel_file = "Growth_Curve_Parameters_and_Sequence_Contribution.xlsx"  # Replace with your file
sheet_name_to_analyze = "Sheet1" # Replace "Sheet1" with the actual name of your sheet
results_df_single_sheet = analyze_single_sheet(excel_file, sheet_name=sheet_name_to_analyze)
results_df_single_sheet.to_csv("categories_single_sheet.csv", index=False)
print("\nResults for single sheet saved to categories_single_sheet.csv")
