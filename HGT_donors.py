from urllib.parse import quote_plus
from Bio import Entrez
import os
import pandas as pd
import time

# --- Configuration ---
# Set your email address (required by NCBI)
Entrez.email = 'harukaru1337@gmail.com' # Please replace with your actual email

# Set your NCBI API key (optional, but recommended)
Entrez.api_key = "efa5c48bcc2ac64d3d8955fc2143c6480d08" # Optional, use after registering with NCBI to increase request rate limit

# --- File and Folder Path Settings ---
input_csv = r"id_16s.csv"  # Input CSV file containing IDs
output_csv = r"id_16s_result.csv" # Output CSV file for results
output_folder = r"donor_16s" # Folder to save downloaded sequences

# --- Script Execution ---
# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the 'id' column from the CSV file
try:
    df = pd.read_csv(input_csv)
    if 'id' not in df.columns:
        raise ValueError("Column 'id' not found in the input CSV file.")
    ids = df['id'].dropna().tolist() # Remove potential NaN values before converting to list
    print(f"Read {len(ids)} IDs from {input_csv}")
except FileNotFoundError:
    print(f"Error: Input file not found at {input_csv}")
    exit()
except ValueError as ve:
    print(ve)
    exit()
except Exception as e:
    print(f"An error occurred while reading the CSV file: {e}")
    exit()


# Initialize the results list
results = []

# Loop through each ID
print("Starting to process IDs and download 16S sequences...")
for i, species_id in enumerate(ids):
    # Ensure species_id is a string, skip if it's not (e.g., if NaN slipped through)
    if not isinstance(species_id, str):
        print(f"Skipping invalid ID at index {i}: {species_id}")
        results.append({"id": species_id, "16s_file": "invalid_id"})
        continue

    print(f"\nProcessing {i+1}/{len(ids)}: {species_id}")
    status = "not_found" # Default status

    try:
        # URL-encode the species ID/name for the query
        encoded_species = quote_plus(species_id)

        # Use Entrez esearch to find 16S sequences in the nuccore database
        # Search term looks for the organism and "16S" in the title
        search_term = f"{encoded_species}[Organism] AND 16S[Title]"
        print(f"Searching nuccore with term: {search_term}")
        handle = Entrez.esearch(db="nuccore", term=search_term, retmax=1) # Get only the top hit
        record = Entrez.read(handle)
        handle.close()

        # Get the UID (Unique Identifier) from the search results
        uid = record['IdList'][0] if record['IdList'] else None

        if uid:
            print(f"Found UID: {uid}")
            # Use the UID to download the 16S sequence using efetch
            print(f"Fetching FASTA sequence for UID {uid}...")
            handle = Entrez.efetch(db="nuccore", id=uid, rettype="fasta", retmode="text")
            fasta_data = handle.read()
            handle.close()

            # Check if FASTA data was successfully retrieved
            if fasta_data and fasta_data.startswith(">"):
                # Prepare the filename
                # Basic sanitization: replace spaces with underscores, remove potentially problematic chars
                safe_species_id = species_id.replace(" ", "_").replace("/", "-").replace("\\", "-")
                fasta_filename_base = f"{safe_species_id}_16s.fasta"
                fasta_filename = os.path.join(output_folder, fasta_filename_base)

                # Save the sequence to the target folder
                with open(fasta_filename, "w", encoding='utf-8') as fasta_file:
                    fasta_file.write(fasta_data)

                status = os.path.basename(fasta_filename) # Record the actual filename saved
                results.append({"id": species_id, "16s_file": status})
                print(f"Success: Downloaded and saved 16S sequence for {species_id} to {fasta_filename}")
            else:
                status = "fasta_download_failed"
                results.append({"id": species_id, "16s_file": status})
                print(f"Warning: Found UID {uid} for {species_id}, but failed to download valid FASTA data.")
        else:
            status = "uid_not_found"
            results.append({"id": species_id, "16s_file": status})
            print(f"Info: No matching UID found for {species_id} with the specified criteria.")

        # Control the request frequency to avoid overloading NCBI servers
        # (Approx. 2 requests per second maximum without API key, potentially more with key)
        time.sleep(0.5)

    except Exception as e:
        # Catch and record any exceptions during processing
        status = f"error:_{str(e)[:50]}" # Record a truncated error message
        results.append({"id": species_id, "16s_file": status})
        print(f"Error processing {species_id}: {e}")
        # Wait a bit longer after an error
        time.sleep(1)

# Write the results to a new CSV file
print("\n--- Processing complete ---")
print(f"Writing results to: {output_csv}")
results_df = pd.DataFrame(results)
try:
    results_df.to_csv(output_csv, index=False, encoding='utf-8-sig') # Use utf-8-sig for better Excel compatibility
    print(f"Task finished! Results summary saved to: {output_csv}")
    print(f"Downloaded FASTA files (if any) are in: {output_folder}")
except Exception as e:
    print(f"Error writing results to CSV file: {e}")
