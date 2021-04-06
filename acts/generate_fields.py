import csv

metadata_filename = '../../../metadata/metadata_ieee8023.csv'
output_filename = 'sed_script_views.py'

# I tried to use Pandas to import the CSV file, but it doesn't seem to correctly handle some blank fields, even when given information about how to handle them.

# isnull gives a dropdown menu with "Unknown," "Yes," and "No" as options. Selecting one of these and pressing Enter does nothing, one has to press Enter on another field or click on the Submit button. It appears that selecting "No" yields records for which there is a non-null value, "Yes" yields records for which the value is "null," and "Unknown" yields both.

with open(metadata_filename,'r') as csv_file:
    with open(output_filename,'w') as output_file:
        print("/^        IMAGE_FIELDS/c\\",file=output_file)
        print("        fields = {\\",file=output_file)
        csv_reader = csv.reader(csv_file,delimiter=',',quotechar='"')
        # default primary key
        print("            'id' : ['exact','in'],\\",file=output_file)
        for headers in csv_reader:
            for header in headers:
                if header in [ 'temperature', 'pO2_saturation', 'leukocyte_count', 'neutrophil_count', 'lymphocyte_count' ]:
                    # float
                    print("            '"+header+"' : ['isnull','gte','lte'],\\",file=output_file)
                elif header in [ 'offset', 'age' ]:
                    # int
                    print("            '"+header+"' : ['isnull','exact','gte','lte'],\\",file=output_file)
                else:
                    # str
                    print("            '"+header+"' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\\",file=output_file)

            print("            }",file=output_file)                    
            break

        print("",file=output_file)       
        print("/^        RESULT_FIELDS/c\\",file=output_file)
        print("        fields = {\\",file=output_file)
        print("            }",file=output_file)                    
        
# Other options that I might not understand
# Regular expressions here use ? to represent a single wildcard character, * to represent multiple wildcard characters, might be based on database backend
# Case-sensitive
# __regex, __startswith, __endswith, __contains,
# Case-insensitive: using these above for strings
# Other
# __in (input field doesn't seem to work well with number fields, since commas are considered invalid, but commas are used to separate values, although apparently not a problem for the automatically-generated primary key)
# __range (the presence of this seems to lead to lots of empty search results, seems like we can just go with both lte and gte, it's more flexible)
# __search (this is Postgres-specific, not sure if there's an advantage over the general regex functionality)
# __gt, __lt (less intuitive than gte and lte, in my opinion)
    
