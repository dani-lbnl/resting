/^        IMAGE_FIELDS/c\
        fields = {\
            'id' : ['exact','in'],\
            'patientid' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'offset' : ['isnull','exact','gte','lte'],\
            'sex' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'age' : ['isnull','exact','gte','lte'],\
            'finding' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'RT_PCR_positive' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'survival' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'intubated' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'intubation_present' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'went_icu' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'in_icu' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'needed_supplemental_O2' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'extubated' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'temperature' : ['isnull','gte','lte'],\
            'pO2_saturation' : ['isnull','gte','lte'],\
            'leukocyte_count' : ['isnull','gte','lte'],\
            'neutrophil_count' : ['isnull','gte','lte'],\
            'lymphocyte_count' : ['isnull','gte','lte'],\
            'view' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'modality' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'date' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'location' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'folder' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'filename' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'doi' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'url' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'license' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'clinical_notes' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            'other_notes' : ['iexact','in','istartswith','icontains','iendswith','iregex','search'],\
            }

/^        RESULT_FIELDS/c\
        fields = {\
            }
