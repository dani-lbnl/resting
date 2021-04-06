import sys
import csv

# I tried to use Pandas to import the CSV file, but it doesn't seem to correctly handle some blank fields, even when given information about how to handle them.

# isnull gives a dropdown menu with "Unknown," "Yes," and "No" as options. Selecting one of these and pressing Enter does nothing, one has to press Enter on another field or click on the Submit button. It appears that selecting "No" yields records for which there is a non-null value, "Yes" yields records for which the value is "null," and "Unknown" yields both.

class csv_processor():

    def __init__(self,input_filename,output_filename):
       
        self.input_filename = input_filename
        self.output_filename = output_filename        
        self.headers = None
        self.reverse_headers = None        
        
    def process_headers(self,row):

        new_row = []

        # Substitute more descriptive names
        for header in row:
            if header == 'folder':
                new_row.append('source_folder')
            elif header == 'filename':
                new_row.append('source_filename')
            elif header == 'url':
                new_row.append('original_url')
            else:
                new_row.append(header)

        # Add thumbnail location columns
        new_row.extend(('thumbnail_folder','thumbnail_filename'))

        return new_row

    def reverse_table(self,headers):

        return_value = {}
        for index in range(len(headers)):
            return_value[headers[index]] = index

        return return_value
    
    def process_record(self,row):

        # Add thumbnail location information
        row.extend((row[self.reverse_headers['source_folder']],row[self.reverse_headers['source_filename']]))

        return row

    def run(self):
        with open(self.input_filename,'r') as input_file:
            csv_reader = csv.reader(input_file,delimiter=',',quotechar='"')
            with open(self.output_filename,'w') as output_file:
                csv_writer = csv.writer(output_file,delimiter=',',quotechar='"')
                start = True
                for row in csv_reader:
                    if start:
                        start = False
                        self.headers = self.process_headers(row)
                        print(self.headers)
                        csv_writer.writerow(self.headers)
                        self.reverse_headers = self.reverse_table(self.headers)
                        print(self.reverse_headers)
                    else:
                        #assert row[self.reverse_headers['source_folder']] == 'image'
                        print(row[self.reverse_headers['source_folder']]) #== 'image')
                        csv_writer.writerow(self.process_record(row))                
    
assert len(sys.argv) == 3
processor = csv_processor(sys.argv[1],sys.argv[2])
processor.run()                
