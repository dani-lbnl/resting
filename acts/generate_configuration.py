import csv

metadata_filename = 'metadata_ieee8023.csv'
output_filename = '../generation/descriptions.py'

# I tried to use Pandas to import the CSV file, but it doesn't seem to correctly handle some blank fields, even when given information about how to handle them.

# isnull gives a dropdown menu with "Unknown," "Yes," and "No" as options. Selecting one of these and pressing Enter does nothing, one has to press Enter on another field or click on the Submit button. It appears that selecting "No" yields records for which there is a non-null value, "Yes" yields records for which the value is "null," and "Unknown" yields both.

indent = '    '

with open(metadata_filename,'r') as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',',quotechar='"')
    # This is just to get the header line, We will break out of this at the end of the first iteration
    for headers in csv_reader:
        with open(output_filename,'w') as output_file:
            print('def return_descriptions():',file=output_file)
            print(indent + 'return_value = {',file=output_file)
            print(indent + indent + "'Image':{",file=output_file)
            # default primary key
            print(indent + indent + indent + "'id' : {",file=output_file)
            print(indent + indent + indent + indent + "'type' : 'models.IntegerField(null=True,blank=True)',",file=output_file)
            print(indent + indent + indent + indent + "'filters' : ['exact','in'],",file=output_file)
            print(indent + indent + indent + indent + "},",file=output_file)            
            for header in headers:
                print(indent + indent + indent + "'" + header + "' : {",file=output_file)                
                if header in [ 'temperature', 'pO2_saturation', 'leukocyte_count', 'neutrophil_count', 'lymphocyte_count' ]:
                    # float
                    print(indent + indent + indent + indent + "'type' : 'models.FloatField(null=True,blank=True)',",file=output_file)                    
                    print(indent + indent + indent + indent + "'filters' : ['isnull','gte','lte'],",file=output_file)
                elif header in [ 'offset', 'age' ]:
                    # int
                    print(indent + indent + indent + indent + "'type' : 'models.IntegerField(null=True,blank=True)',",file=output_file)                                        
                    print(indent + indent + indent + indent + "'filters' : ['isnull','exact','gte','lte'],",file=output_file)
                else:
                    # str
                    print(indent + indent + indent + indent + "'type' : 'models.CharField(max_length=256,blank=True)',",file=output_file)
                    print(indent + indent + indent + indent + "'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],",file=output_file)
                    
                print(indent + indent + indent + indent + '},',file=output_file)
                
            print(indent + indent + indent + '}',file=output_file)
            
            print(indent + indent + '}',file=output_file)

            print(indent + 'return return_value',file=output_file)
            
        break
    
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
    
