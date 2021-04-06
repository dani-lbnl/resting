import csv
import rest_client

metadata_filename = '../metadata/metadata_ieee8023.csv'

# I tried to use Pandas to import the CSV file, but it doesn't seem to correctly handle some blank fields, even when given information about how to handle them.

with open(metadata_filename,'r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',',quotechar='"')
    headers = None
    records = []
    for row in csv_reader:
        if headers == None:
            headers = row
            column_data_types = []
            for header in headers:
                if header in [ 'temperature', 'pO2_saturation', 'leukocyte_count', 'neutrophil_count', 'lymphocyte_count' ]:
                    column_data_types.append(float)
                elif header in [ 'offset', 'age' ]:
                    column_data_types.append(int)
                else:
                    column_data_types.append(str)
        else:
            converted_row = []
            for column_number in range(len(headers)):
                if column_data_types[column_number] == str:
                    converted_row.append(row[column_number])
                elif column_data_types[column_number] == float:
                    if row[column_number] == '':
                        converted_row.append(None)
                    else:
                        converted_row.append(float(row[column_number]))
                else:
                    if row[column_number] == '':
                        converted_row.append(None)
                    else:
                        converted_row.append(int(row[column_number]))
            records.append(converted_row)

server = 'covidscreen.lbl.gov'

username = 'khiga'
password = 'gN03#AwJ!Wla'

authenticated_database_connection = rest_client.DatabaseConnection(server,username=username,password=password)

print(authenticated_database_connection.authenticated_relative_request_and_receive('image/'))

# It appears that the serializers only handle one dictionary-like object at a time, so generate a dictionary from each record and store it.

for record in records:
    unencoded_data = {}
    for column_number in range(len(headers)):
        value = record[column_number]
        unencoded_data[headers[column_number]] = value

    authenticated_database_connection.authenticated_relative_request_and_receive('image/',unencoded_data=unencoded_data)
