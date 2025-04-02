import pandas as pd
from scipy import stats

def perform_anova_on_excel(excel_file, columns_to_analyze):
    """
    Perform one-way ANOVA on specified columns in an Excel file.

    Args:
        excel_file (str): Path to the Excel file (.xlsx or .xls).
        columns_to_analyze (list of int): List of column indices to analyze (starting from 1).

    Returns:
        tuple: A tuple containing the F-statistic and P-value.
               Returns None, None if an error occurs.
    """
    try:
        # 1. Read Excel file
        df = pd.read_excel(excel_file)

        # 2. Extract data columns to be analyzed
        data_columns = []
        for col_index in columns_to_analyze:
            # pandas column index starts from 0, so col_index - 1 is needed
            if col_index <= len(df.columns): # Check if column index is valid
                data_columns.append(df.iloc[:, col_index - 1].dropna()) # Extract column data and remove NaN values
            else:
                print(f"Warning: Column index {col_index} exceeds the column range of the Excel file. This column has been skipped.")
                continue # Skip invalid column index

        if len(data_columns) < 2: # ANOVA requires at least two groups of data
            print("Error: At least two valid data columns are required to perform ANOVA.")
            return None, None

        # 3. Perform one-way ANOVA (f_oneway)
        f_statistic, p_value = stats.f_oneway(*data_columns) # Use * to unpack the list as arguments for f_oneway

        # 4. Return results
        return f_statistic, p_value

    except FileNotFoundError:
        print(f"Error: Excel file '{excel_file}' not found. Please check if the file path is correct.")
        return None, None
    except Exception as e:
        print(f"An unknown error occurred: {e}")
        return None, None

if __name__ == "__main__":
    excel_file_path = "mfuzz_anova.xlsx"  # Replace with your Excel file path
    columns_to_analyze = [1, 2, 3, 4, 5]  # Columns to be analyzed, here are columns 1-5

    f_stat, p_val = perform_anova_on_excel(excel_file_path, columns_to_analyze)

    if f_stat is not None and p_val is not None:
        print("One-way ANOVA results:")
        print(f"F Statistic: {f_stat:.4f}") # Keep 4 decimal places
        print(f"P-value: {p_val:.4f}")   # Keep 4 decimal places

        alpha = 0.05  # Common significance level
        if p_val < alpha:
            print(f"P-value ({p_val:.4f}) is less than the significance level ({alpha}), reject the null hypothesis.")
            print("Conclusion: There is a significant difference in the means of gene expression levels among different co-culture distance groups.")
            print("Suggestion: If you need to further understand which groups have specific differences, please perform post-hoc tests (e.g., Tukey's HSD).")
        else:
            print(f"P-value ({p_val:.4f}) is greater than or equal to the significance level ({alpha}), fail to reject the null hypothesis.")
            print("Conclusion: There is not enough evidence to show a significant difference in the means of gene expression levels among different co-culture distance groups.")
            print("Note: This does not mean there is no difference between groups, but the current data cannot provide sufficient statistical evidence.")

        print("\nPlease note: ANOVA has prerequisite assumptions (normality and homogeneity of variance).")
        print("For the reliability of the results, please ensure to check if your data meets these assumptions.")
        print("If not met, data transformation or non-parametric tests may need to be considered.")
