import os
import csv

# Define file paths
input_dir = '/public/home/wuq8022600160/Leech/NCBI_Lp/ffn_cog/'
output_file_path = 'sequence_contribution.csv'

# Specific COG categories
cog_categories = ['J', 'K', 'L', 'C', 'E', 'F', 'G', 'H', 'I', 'P', 'Q', 'D', 'M', 'N', 'O', 'T', 'U', 'V']

# Create a dictionary to store the total sequence length for each COG category
cog_lengths = {cog: 0 for cog in cog_categories}

# Process each ffn file
file_results = []

for filename in os.listdir(input_dir):
    if filename.endswith('.ffn'):
        input_file_path = os.path.join(input_dir, filename)

        # Initialize total sequence length for each COG category for the current file
        current_lengths = {cog: 0 for cog in cog_categories}

        with open(input_file_path, mode='r', encoding='utf-8') as f_in:
            lines = f_in.readlines()
            sequence = ''
            current_cog = None

            for line in lines:
                if line.startswith('>'):  # Process description line
                    if sequence:  # If there is current sequence data, count its length
                        if current_cog in current_lengths:
                            current_lengths[current_cog] += len(sequence)
                    sequence = ''  # Clear sequence line
                    # Extract COG information from the description line
                    for cog in cog_categories:
                        if cog in line:
                            current_cog = cog
                            break
                    else:
                        current_cog = None  # If no COG matched
                else:
                    sequence += line.strip()  # Append sequence line (remove newline character)

            # Process the last sequence
            if sequence and current_cog:
                if current_cog in current_lengths:
                    current_lengths[current_cog] += len(sequence)

        # Save results for the current file
        file_results.append([filename] + [current_lengths[cog] for cog in cog_categories])

# Write the results to a CSV file
with open(output_file_path, mode='w', newline='', encoding='utf-8') as f_out:
    writer = csv.writer(f_out)
    # Write header line
    writer.writerow(['File Name'] + cog_categories)
    # Write statistical data for each file
    writer.writerows(file_results)

print("Processing completed, results saved to", output_file_path)
