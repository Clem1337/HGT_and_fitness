import pandas as pd

# Read CSV file
file_path = 'All_HGT_present_absence.csv'
data = pd.read_csv(file_path)

# Initialize dictionary for statistical results
cog_functions = 'J.K.L.C.E.F.G.H.I.P.Q.D.M.N.O.T.U.V.S'.split('.')
cog_counts = {func: {i: 0 for i in range(1, 307)} for func in cog_functions}
total_counts = {i: 0 for i in range(1, 307)}

# Iterate through data to count the occurrences of specified functions in the COG column for each 'No. isolates' value
for index, row in data.iterrows():
    no_isolates = row['No. isolates']
    cog_value = str(row['COG'])  # Convert the COG column value to a string
    for i in range(1, 307):
        if no_isolates >= i:
            total_counts[i] += 1  # Count the total number of entries for each 'No. isolates' value
            for func in cog_functions:
                if func in cog_value:
                    cog_counts[func][i] += 1

# Prepare output data
output_data = {'No. isolates': list(range(1, 307))}
for func in cog_functions:
    output_data[f'{func}_Count'] = [cog_counts[func][i] for i in range(1, 307)]
output_data['Total_Count'] = [total_counts[i] for i in range(1, 307)]

# Create DataFrame and save to CSV file
output_df = pd.DataFrame(output_data)
output_file_path = 'HGT_Functional_Gene_Counts.csv'
output_df.to_csv(output_file_path, index=False)
print(f'Results saved to {output_file_path}')
