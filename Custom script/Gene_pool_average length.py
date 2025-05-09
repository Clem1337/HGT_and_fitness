import pandas as pd

# Read CSV file
file_path = 'All_HGT_present_absence.csv'
data = pd.read_csv(file_path)

# Initialize dictionary for statistical results
cog_functions = 'J.K.L.C.E.F.G.H.I.P.Q.D.M.N.O.T.U.V.S'.split('.')
cog_avg_nuc = {func: {i: 0 for i in range(1, 307)} for func in cog_functions}
overall_avg_nuc = {i: 0 for i in range(1, 307)}

# Iterate through data to calculate the average 'Avg group size nuc' when 'No. isolates' column containing specified functions in COG is greater than or equal to a specified value
for i in range(1, 307):
    filtered_data = data[data['No. isolates'] >= i]
    overall_avg_nuc[i] = filtered_data['Avg group size nuc'].mean()
    for func in cog_functions:
        cog_filtered_data = filtered_data[filtered_data['COG'].str.contains(func, na=False)]
        if not cog_filtered_data.empty:
            cog_avg_nuc[func][i] = cog_filtered_data['Avg group size nuc'].mean()

# Prepare output data
output_data = {'No. isolates': list(range(1, 307))}
for func in cog_functions:
    output_data[f'{func}_Avg_Nuc'] = [cog_avg_nuc[func][i] for i in range(1, 307)]
output_data['Overall_Avg_Nuc'] = [overall_avg_nuc[i] for i in range(1, 307)]

# Create DataFrame and save to CSV file
output_df = pd.DataFrame(output_data)
output_file_path = 'HGT_Average_Length.csv'
output_df.to_csv(output_file_path, index=False)
print(f'Results saved to {output_file_path}')
