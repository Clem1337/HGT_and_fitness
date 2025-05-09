import pandas as pd

# Read CSV file
file_path = 'All_HGT_present_absence.csv'
data = pd.read_csv(file_path)

# COG functional gene cluster classification
cog_functions = 'J.K.L.C.E.F.G.H.I.P.Q.D.M.N.O.T.U.V.S'.split('.')
cog_functions.append('Total')

# Initialize result dictionary
cog_ratios = {func: {i: 0 for i in range(1, 307)} for func in cog_functions}

# Iterate through each No. isolates value
for i in range(1, 307):
    filtered_data = data[data['No. isolates'] >= i]
    total_genes = len(filtered_data)

    for func in cog_functions:
        if func == 'Total':
            cog_ratios[func][i] = total_genes
        else:
            cog_filtered_data = filtered_data[filtered_data['COG'].str.contains(func, na=False)]
            if total_genes > 0:
                cog_ratios[func][i] = len(cog_filtered_data) / total_genes
            else:
                cog_ratios[func][i] = 0

# Prepare output data
output_data = {'No. isolates': list(range(1, 307))}
for func in cog_functions:
    output_data[f'{func}_Ratio'] = [cog_ratios[func][i] for i in range(1, 307)]

# Create DataFrame and save to CSV file
output_df = pd.DataFrame(output_data)
output_file_path = 'HGT_Functional_Gene_Ratio.csv'
output_df.to_csv(output_file_path, index=False)
print(f'Results saved to {output_file_path}')
