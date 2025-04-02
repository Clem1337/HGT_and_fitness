from Bio import Entrez
import pandas as pd

# Set Entrez API parameters
Entrez.email = "harukaru1337@gmail.com"
Entrez.api_key = ""  # If you have an API Key

# Read CSV file
input_file = "only_aggregated_deduplicated_result3.csv"
data = pd.read_csv(input_file)

# Extract ID column
ids = data['id']

# Prepare to store results
taxonomy_results = []

# Query taxonomic information for each ID
for index, organism in enumerate(ids):
    try:
        print(f"Processing {index + 1}/{len(ids)}: {organism}...")  # Print current progress

        # eSearch: Get Taxonomy ID
        handle = Entrez.esearch(db="taxonomy", term=organism, retmode="xml")
        record = Entrez.read(handle)
        handle.close()

        if record['IdList']:
            tax_id = record['IdList'][0]

            # eFetch: Get detailed taxonomic information
            handle = Entrez.efetch(db="taxonomy", id=tax_id, retmode="xml")
            record = Entrez.read(handle)
            handle.close()

            tax_data = record[0]
            lineage = {entry['Rank']: entry['ScientificName'] for entry in tax_data['LineageEx']}

            # Extract specified taxonomic levels
            phylum = lineage.get('phylum', 'NA')
            class_ = lineage.get('class', 'NA')
            order = lineage.get('order', 'NA')
            family = lineage.get('family', 'NA')
            genus = lineage.get('genus', 'NA')
            species = tax_data.get('ScientificName', 'NA')  # Species is the current node

            taxonomy_results.append((organism, phylum, class_, order, family, genus, species))
            print(f"Result: Phylum={phylum}, Class={class_}, Order={order}, Family={family}, Genus={genus}, Species={species}")
        else:
            taxonomy_results.append((organism, "Not found", "Not found", "Not found", "Not found", "Not found", "Not found"))
            print(f"No Taxonomy ID found for {organism}")

    except Exception as e:
        taxonomy_results.append((organism, f"Error: {str(e)}", "NA", "NA", "NA", "NA", "NA"))
        print(f"Error processing {organism}: {str(e)}")

# Save results to a new CSV file
output_file = "only_aggregated_deduplicated_result4.csv"
result_df = pd.DataFrame(taxonomy_results, columns=['Organism', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'])
result_df.to_csv(output_file, index=False)

print(f"Processing complete. Results saved to {output_file}")
