app_name = 'database'

# Description format:
# { 
#     ModelName_str : {
#         ModelAttribute_str : {
#             "type" : Instanciation_str,
#             "filters" : [ FilterName_str, ... ]
#         }, ...
#     }, ...
# }

models = {
    'Source':{
        'patientid' : {
            'type' : 'models.CharField(max_length=32,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'offset' : {
            'type' : 'models.IntegerField(null=True,blank=True)',
            'filters' : ['isnull','exact','gte','lte'],
            },
        'sex' : {
            'type' : 'models.CharField(max_length=2,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'age' : {
            'type' : 'models.IntegerField(null=True,blank=True)',
            'filters' : ['isnull','exact','gte','lte'],
            },
        'finding' : {
            'type' : 'models.CharField(max_length=128,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'RT_PCR_positive' : {
            'type' : 'models.CharField(max_length=16,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'survival' : {
            'type' : 'models.CharField(max_length=1,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'intubated' : {
            'type' : 'models.CharField(max_length=1,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'intubation_present' : {
            'type' : 'models.CharField(max_length=1,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'went_icu' : {
            'type' : 'models.CharField(max_length=1,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'in_icu' : {
            'type' : 'models.CharField(max_length=1,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'needed_supplemental_O2' : {
            'type' : 'models.CharField(max_length=1,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'extubated' : {
            'type' : 'models.CharField(max_length=1,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'temperature' : {
            'type' : 'models.FloatField(null=True,blank=True)',
            'filters' : ['exact','isnull','gte','lte'],
            },
        'pO2_saturation' : {
            'type' : 'models.FloatField(null=True,blank=True)',
            'filters' : ['exact','isnull','gte','lte'],
            },
        'leukocyte_count' : {
            'type' : 'models.FloatField(null=True,blank=True)',
            'filters' : ['exact','isnull','gte','lte'],
            },
        'neutrophil_count' : {
            'type' : 'models.FloatField(null=True,blank=True)',
            'filters' : ['exact','isnull','gte','lte'],
            },
        'lymphocyte_count' : {
            'type' : 'models.FloatField(null=True,blank=True)',
            'filters' : ['exact','isnull','gte','lte'],
            },
        'view' : {
            'type' : 'models.CharField(max_length=32,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'modality' : {
            'type' : 'models.CharField(max_length=16,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'date' : {
            'type' : 'models.CharField(max_length=32,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'location' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'folder' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'filename' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'doi' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'url' : {
            'type' : 'models.URLField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'license' : {
            'type' : 'models.CharField(max_length=64,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'clinical_notes' : {
            'type' : 'models.TextField(max_length=8192,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'other_notes' : {
            'type' : 'models.TextField(max_length=2048,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'thumbnail_folder' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'thumbnail_filename' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'artifacts_and_distortion': {
            'type': 'models.CharField(max_length=128,blank=True)',
            'filters': ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search']
            },
        'notes': {
            'type': 'models.TextField(max_length=1024,blank=True)',
            'filters': ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search']
            },
        'thumbnail_filename_wildcard': {
            'type': 'models.CharField(max_length=32,blank=True)',
            'filters': ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search']
            },
        },
    'Result':{
        'directory' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'filename' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'method' : {
            'type' : 'models.CharField(max_length=256,blank=True)',
            'filters' : ['exact','iexact','in','istartswith','icontains','iendswith','iregex','search'],
            },
        'source' : {
            # Can map many Result instances to a single Source instance
            'type' : 'models.ForeignKey(Source,related_name="results",on_delete=models.CASCADE)',
            'filters' : [],
            },
        'test_sources' : {
            # Can map many Result instances to many Source instances
            'type' : 'models.ManyToManyField(Source,related_name="test_results")',
            'filters' : [],
            },        
        }
    }
