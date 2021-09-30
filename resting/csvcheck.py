import project
import sys
import csv

len_sys_argv = len(sys.argv)

if len_sys_argv == 2:
    print('Usage:',sys.executable,sys.argv[0],'<model name> <CSV file 1> [CSV file 2] [CSV file 3] ...')
    exit()

greatest_lengths = {}
for csv_filename_index in range(2,len_sys_argv):
    with open(sys.argv[csv_filename_index],'r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')        
        have_headers = False
        header_length_limits = []
        len_record = 0
        for record in csv_reader:
            if not have_headers:
                header_length_limits = [ 0 for header in record ]
                have_headers = True
                len_record = len(record)
                headers = record
            else:
                for field_number in range(len_record):
                    len_field = len(record[field_number])
                    if len_field > header_length_limits[field_number]:
                        header_length_limits[field_number] = len_field
        for field_number in range(len_record):
            header = headers[field_number]
            if header in greatest_lengths:
                if header_length_limits[field_number] > greatest_lengths[header]:
                    greatest_lengths[header] = header_length_limits[field_number]
            else:
                greatest_lengths[header] = header_length_limits[field_number]
print(greatest_lengths)

for header in greatest_lengths:
    try:
        type_string = project.models[sys.argv[1]][header]['type']
        max_length_keyword_position = type_string.find('max_length=')
        if max_length_keyword_position != -1:
            max_length_end_position = type_string.find(',',max_length_keyword_position+11)
            max_length = int(type_string[max_length_keyword_position+11:max_length_end_position])
            if max_length < greatest_lengths[header]:
                print(header,'field length is too short')
    except:
        pass

