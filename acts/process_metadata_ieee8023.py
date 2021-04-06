import csv

original_filename = 'metadata_ieee8023.csv'
modified_filename = 'processed_metadata_ieee8023.csv'

field_lengths_filename = 'field_lengths.py'

replacement_header_line = 'patientid,offset,sex,age,finding,RT_PCR_positive,survival,intubated,intubation_present,went_icu,in_icu,needed_supplemental_O2,extubated,temperature,pO2_saturation,leukocyte_count,neutrophil_count,lymphocyte_count,view,modality,date,location,folder,filename,doi,url,license,clinical_notes,other_notes,thumbnail_folder,thumbnail_filename\n'

column_count = 31

with open(original_filename,'r') as input_file:
    with open(modified_filename,'w') as output_file:
        header_line = input_file.readline().rstrip()
        output_file.write(replacement_header_line)
        csv_reader = csv.reader(input_file,delimiter=',',quotechar='"')
        csv_writer = csv.writer(output_file,delimiter=',',quotechar='"')
        maximum_lengths = [ 0 for i in range(column_count) ]
        for row in csv_reader:
            row.extend(['/global/cfs/cdirs/m3670/CXR/datasets/covid-chestxray-dataset/'+row[22],row[23]])
            csv_writer.writerow(row)
            lengths = [ len(element) for element in row ]
            for col in range(column_count):
                if lengths[col] > maximum_lengths[col]:
                    maximum_lengths[col] = lengths[col]

with open(field_lengths_filename,'a') as lengths_file:
    print('#',replacement_header_line,file=lengths_file)
    print('#',modified_filename,maximum_lengths,file=lengths_file)
