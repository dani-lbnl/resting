import csv

output_filename = 'project_Source.py'

all_headers = {}

for filename in ['processed_metadata_ieee8023.csv','processed_actual_metadata.csv','processed_COVID-19.metadata.csv','processed_figure_metadata.csv']:

    with open(filename,'r') as csv_file:

        csv_reader = csv.reader(csv_file)

        for row in csv_reader:

            for attribute in row:
                if attribute not in all_headers:
                    all_headers[attribute] = {'type':'','filters':[]}

            # Only want to examine the header lien
            break

with open(output_filename,'w') as header_file:
    print({'Source':all_headers},file=header_file)
