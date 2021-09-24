import project
import sys
import csv

len_sys_argv = len(sys.argv)

if len_sys_argv == 2:
    print('Usage:',sys.executable,sys.argv[0],'<model name> <CSV file 1> [CSV file 2] [CSV file 3] ...')
    exit()

for csv_filename_index in range(2,len_sys_argv):
    with open(sys.argv[csv_filename_index],'r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')        
        #header_line = next(csv_file)
        #print(header_line[0])
        have_headers = False
        for record in csv_reader:
            if not have_headers:
                have_headers = True
                for header in record:
                    print(sys.argv[1])
                    print(project.models)
                    type_string = project.models[sys.argv[1]][header]['type']
                    max_length_keyword_position = type_string.find('max_length=')
                    if max_length_keyword_position != -1:
                        max_length_end_position = type_string.find(',',max_length_keyword_position+11)
                        max_length = int(type_string[max_length_keyword_position+11:max_length_end_position])
                        print(max_length)
                exit()
            else:
                exit()
