import pandas
import numpy
import math

metadata_filename = 'metadata_ieee8023.csv'

metadata = pandas.read_csv(metadata_filename)

with open('models.py','w') as output_file:
    print('class Image(models.Model):',file=output_file)
    for i in metadata.columns:
        data_type = type(metadata[i][0])

        if data_type == numpy.float64:
            all_ints = True            
            for entry in metadata[i]:

                if not math.isnan(entry) and (math.floor(entry) != entry):
                    all_ints = False
                    break
                
            if all_ints:
                if min(metadata[i]) >= 0 and max(metadata[i]) <= 32767:
                    print('    ' + i + ' = models.PositiveSmallIntegerField(null=True,blank=True)',file=output_file)
                elif min(metadata[i]) >= -32768 and max(metadata[i]) <= 32767:
                    print('    ' + i + ' = models.SmallIntegerField(null=True,blank=True)',file=output_file)                    
                else:
                    print('    ' + i + ' = models.IntegerField(null=True,blank=True)',file=output_file)
            else:
                print('    ' + i + ' = models.FloatField(null=True,blank=True)',file=output_file)
                    
        else:
            lengths = metadata[i].str.len()
            longest = 0
            for l in lengths:
                if not math.isnan(l) and l > longest:
                    longest = int(l)
            print('    ' + i + ' = models.CharField(max_length=',longest,',blank=True)',file=output_file)

#for i in metadata.columns:
#    print(i,len(metadata.groupby(i).groups.keys()))
