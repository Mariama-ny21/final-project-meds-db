import csv

input_file = 'UK_Medicines_with_BNF_relaxed_filled.csv'
output_file = 'UK_Medicines_with_BNF_emc.csv'

def emc_search_url(medicine_name):
    # EMC search URL for the medicine name
    base_url = 'https://www.medicines.org.uk/emc/search?q='
    return base_url + medicine_name.replace(' ', '+')

def add_emc_urls():
    with open(input_file, newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['emc_leaflet_url'] if 'emc_leaflet_url' not in reader.fieldnames else reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            med_name = row['medicine_name']
            row['emc_leaflet_url'] = emc_search_url(med_name)
            writer.writerow(row)
    print(f"EMC URLs added. Output written to {output_file}")

if __name__ == '__main__':
    add_emc_urls()
