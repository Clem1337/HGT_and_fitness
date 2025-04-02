import pandas as pd
from scipy.stats import fisher_exact

def perform_fisher_enrichment_for_column(df, column_index):
    """
    Perform Fisher's exact test to detect if data in the specified column of a DataFrame is enriched in the range > 0.5.
    Background values are taken from all columns in the DataFrame except the specified column.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        column_index (int): Index of the column to be tested (starting from 0).

    Returns:
        tuple: A tuple containing Fisher's exact test results (oddsratio, pvalue),
               and the constructed 2x2 contingency table DataFrame.
               Returns None, None, None if the column index is invalid.
    """
    num_cols = df.shape[1]
    if column_index < 0 or column_index >= num_cols:
        print(f"Error: Specified column index {column_index} is out of range (0 to {num_cols-1}).")
        return None, None, None

    try:
        target_column = df.iloc[:, column_index]
        background_columns_list = []
        for i in range(num_cols):
            if i != column_index:
                background_columns_list.append(df.iloc[:, i])
        background_columns = pd.concat(background_columns_list, axis=1).values.flatten()

    except IndexError:
        print("Error: Column index out of range. Please check DataFrame column count.")
        return None, None, None

    # Ensure data is numeric type, if not, try to convert to numeric and handle conversion failures
    try:
        target_column_numeric = pd.to_numeric(target_column, errors='coerce').dropna()
        background_numeric = pd.to_numeric(pd.Series(background_columns), errors='coerce').dropna() # Convert background data to Series and handle NaN
    except Exception as e:
        print(f"Data type conversion error: {e}. Please ensure that the relevant columns contain numeric data.")
        return None, None, None

    if target_column_numeric.empty or background_numeric.empty:
        print("Warning: After numeric conversion, the target column or background data is empty. Please check if there is non-numeric data in the data.")
        return None, None, None


    # Construct 2x2 contingency table
    observed_above_05_target = target_column_numeric[target_column_numeric > 0.5].count()
    observed_below_equal_05_target = target_column_numeric[target_column_numeric <= 0.5].count()
    observed_above_05_background = background_numeric[background_numeric > 0.5].count()
    observed_below_equal_05_background = background_numeric[background_numeric <= 0.5].count()

    contingency_table = [[observed_above_05_target, observed_above_05_background],
                         [observed_below_equal_05_target, observed_below_equal_05_background]]

    # Perform Fisher's exact test (one-tailed test, testing for enrichment, i.e., alternative='greater')
    oddsratio, pvalue = fisher_exact(contingency_table, alternative='greater')

    # Construct DataFrame-formatted contingency table for easy display
    contingency_df = pd.DataFrame(contingency_table,
                                  index=['>0.5', '<=0.5'],
                                  columns=['Target Column', 'Background (Other Columns)'])

    return oddsratio, pvalue, contingency_df


if __name__ == "__main__":
    excel_file_path = "complementary_and_config.xlsx"  # Replace with your Excel file path
    sheet_name = "raw data" # Specify Sheet name
    output_csv_file = "complementary_ratio_enrichment.csv" # Output CSV file name
    results_data = [] # List to store result data

    try:
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error occurred while reading Excel file: {e}")
        exit()

    start_column_index = 1  # Index of the second column (starting from 0)
    end_column_index = 18   # Index of the 19th column (starting from 0)

    for column_index in range(start_column_index, end_column_index + 1):
        col_name = df.columns[column_index] if column_index < len(df.columns) else f"Column {column_index + 1}" # Get column name, use default name if index out of range
        odds_ratio, p_value, table = perform_fisher_enrichment_for_column(df, column_index)

        if odds_ratio is not None:
            results_data.append([col_name, p_value]) # Store column name and p-value
            print(f"Column: '{col_name}' (Index: {column_index + 1}) - Fisher's Exact Test Results:")
            print("-----------------------------------")
            print("2x2 Contingency Table:")
            print(table)
            print("\nOdds Ratio: {:.4f}".format(odds_ratio))
            print("P-value (One-tailed, testing for enrichment in >0.5): {:.4f}".format(p_value))
            print("-----------------------------------")

            alpha = 0.05  # Significance level
            if p_value < alpha:
                print(f"P-value ({p_value:.4f}) < Significance level ({alpha}), reject the null hypothesis.")
                print(f"Conclusion: Column '{col_name}' (Index: {column_index + 1}) data is significantly enriched in the range > 0.5 (compared to background values).")
            else:
                print(f"P-value ({p_value:.4f}) >= Significance level ({alpha}), fail to reject the null hypothesis.")
                print(f"Conclusion: There is not enough evidence to show that Column '{col_name}' (Index: {column_index + 1}) data is significantly enriched in the range > 0.5 (compared to background values).")
        else:
            print(f"Column: '{col_name}' (Index: {column_index + 1}) - Fisher's Exact Test failed to execute successfully, please check error messages.")
        print("\n" + "="*50 + "\n") # Separator for each column's results

    # Create DataFrame and save to CSV
    results_df = pd.DataFrame(results_data, columns=['Column Name', 'P-value'])
    results_df.to_csv(output_csv_file, index=False) # index=False prevents writing row index

    print(f"Results saved to CSV file: '{output_csv_file}'")
