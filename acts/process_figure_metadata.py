import csv

original_filename = 'figure_metadata.csv'
modified_filename = 'processed_figure_metadata.csv'

field_lengths_filename = 'field_lengths.py'

replacement_header_line = 'patientid,offset,sex,age,finding,survival,temperature,pO2_saturation,view,modality,artifacts_and_distortion,notes,thumbnail_folder,thumbnail_filename_stub\n'

column_count = 14

with open(original_filename,'r',encoding='ISO-8859-1') as input_file:
    with open(modified_filename,'w') as output_file:
        header_line = input_file.readline().rstrip()
        output_file.write(replacement_header_line)
        csv_reader = csv.reader(input_file,delimiter=',',quotechar='"')
        csv_writer = csv.writer(output_file,delimiter=',',quotechar='"')
        maximum_lengths = [ 0 for i in range(column_count) ]
        for row in csv_reader:
            row.extend(['/global/cfs/cdirs/m3670/CXR/datasets/Figure1-COVID-chestxray-dataset/images',row[0]+'.*'])
            csv_writer.writerow(row)
            lengths = [ len(element) for element in row ]
            for col in range(column_count):
                if lengths[col] > maximum_lengths[col]:
                    maximum_lengths[col] = lengths[col]

with open(field_lengths_filename,'a') as lengths_file:
    print('#',replacement_header_line,file=lengths_file)
    print('#',modified_filename,maximum_lengths,file=lengths_file)
    
