def return_description():
    return_value = {
        'Image':{
            'id' : {
                'filters' : ['exact','in'],
                },
            'patientid' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'offset' : {
                'type' : 'models.IntegerField(null=True,blank=True)',
                'filters' : ['isnull','exact','gte','lte'],
                },
            'sex' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'age' : {
                'type' : 'models.IntegerField(null=True,blank=True)',
                'filters' : ['isnull','exact','gte','lte'],
                },
            'finding' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'RT_PCR_positive' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'survival' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'intubated' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'intubation_present' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'went_icu' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'in_icu' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'needed_supplemental_O2' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'extubated' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'temperature' : {
                'type' : 'models.FloatField(null=True,blank=True)',
                'filters' : ['isnull','gte','lte'],
                },
            'pO2_saturation' : {
                'type' : 'models.FloatField(null=True,blank=True)',
                'filters' : ['isnull','gte','lte'],
                },
            'leukocyte_count' : {
                'type' : 'models.FloatField(null=True,blank=True)',
                'filters' : ['isnull','gte','lte'],
                },
            'neutrophil_count' : {
                'type' : 'models.FloatField(null=True,blank=True)',
                'filters' : ['isnull','gte','lte'],
                },
            'lymphocyte_count' : {
                'type' : 'models.FloatField(null=True,blank=True)',
                'filters' : ['isnull','gte','lte'],
                },
            'view' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'modality' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'date' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'location' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'folder' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'filename' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'doi' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'url' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'license' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'clinical_notes' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            'other_notes' : {
                'type' : 'models.CharField(max_length=256,blank=True)',
                'filters' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],
                },
            }
        }
    return return_value
