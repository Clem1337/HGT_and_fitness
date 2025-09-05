import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# --- File and column settings ---
input_csv_file = 'phenotype_results.csv'
output_excel_file = 'regression_analysis.xlsx'

# Define the dependent variable (to be explained)
dependent_var = 'RTT distance'
# Define independent variables (used to explain)
independent_vars = ['hgt_rtt', 'nhgt_rtt']

try:
    # --- 1. Load and prepare the data ---
    df = pd.read_csv(input_csv_file)

    # Check if all required columns exist
    required_columns = [dependent_var] + independent_vars
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"The following required columns are missing from the input file: {', '.join(missing_cols)}")

    # Remove rows with missing values (NaN) in the relevant columns
    df_clean = df[required_columns].dropna()

    # Ensure there's enough data left to run the regression
    if len(df_clean) < len(independent_vars) + 2:
        raise ValueError("Not enough data to perform regression analysis after removing missing values.")

    # --- 2. Build and fit the multiple linear regression model ---
    # Construct the formula using R-style syntax. Q() ensures proper handling of column names with spaces
    formula = f"Q('{dependent_var}') ~ {' + '.join(independent_vars)}"

    # Use statsmodels' OLS (ordinary least squares) to build the model
    model = smf.ols(formula=formula, data=df_clean)

    # Fit the model and get the results
    results = model.fit()

    # --- 3. Extract and organize results ---
    # Overall model statistics
    summary_data = {
        'Metric': [
            'R-squared',
            'Adjusted R-squared',
            'F-statistic',
            'Prob (F-statistic)',
            'Number of observations'
        ],
        'Value': [
            results.rsquared,
            results.rsquared_adj,
            results.fvalue,
            results.f_pvalue,
            int(results.nobs)
        ]
    }
    summary_df = pd.DataFrame(summary_data)

    # Extract coefficients, p-values, etc.
    coeffs_df = results.summary2().tables[1]
    coeffs_df = coeffs_df.reset_index().rename(columns={'index': 'Variable'})

    # --- 4. Output to Excel ---
    # Write both summary and coefficients to a single Excel sheet
    with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
        # Write model summary
        summary_df.to_excel(writer, sheet_name='Regression Results', index=False, startrow=0)
        
        # Write coefficients two rows below the summary
        coeffs_df.to_excel(writer, sheet_name='Regression Results', index=False, startrow=len(summary_df) + 2)

    print(f"Regression analysis completed! Results have been successfully saved to: {output_excel_file}")
    print("\n--- Model Summary ---")
    # Print key stats to console
    print(f"R-squared: {results.rsquared:.4f}")
    print(f"Adjusted R-squared: {results.rsquared_adj:.4f}")
    print(f"\nFor the full report, please see the file '{output_excel_file}'.")

except FileNotFoundError:
    print(f"Error: The input file '{input_csv_file}' was not found. Please ensure it is located in the same directory as the script.")
except ValueError as ve:
    print(f"Value Error: {ve}")
except Exception as e:
    print(f"An unexpected error occurred during processing: {e}")
