
from rest_framework import viewsets, permissions
import rest_framework_filters
from database.models import *
from database.serializers import *

class SourceFilter(rest_framework_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'patientid': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'offset': ['isnull', 'exact', 'gte', 'lte'],
            'sex': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'age': ['isnull', 'exact', 'gte', 'lte'],
            'finding': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'RT_PCR_positive': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'survival': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'intubated': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'intubation_present': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'went_icu': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'in_icu': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'needed_supplemental_O2': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'extubated': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'temperature': ['exact', 'isnull', 'gte', 'lte'],
            'pO2_saturation': ['exact', 'isnull', 'gte', 'lte'],
            'leukocyte_count': ['exact', 'isnull', 'gte', 'lte'],
            'neutrophil_count': ['exact', 'isnull', 'gte', 'lte'],
            'lymphocyte_count': ['exact', 'isnull', 'gte', 'lte'],
            'view': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'modality': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'date': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'location': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'folder': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'filename': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'doi': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'url': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'license': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'clinical_notes': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'other_notes': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'thumbnail_folder': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'thumbnail_filename': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'artifacts_and_distortion': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'notes': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'thumbnail_filename_wildcard': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            }

class SourceViewSet(viewsets.ModelViewSet):
    filter_class = SourceFilter
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ResultFilter(rest_framework_filters.FilterSet):
    class Meta:
        model = Result
        fields = {
            'directory': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'filename': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            'method': ['exact', 'iexact', 'in', 'istartswith', 'icontains', 'iendswith', 'iregex', 'search'],
            }

class ResultViewSet(viewsets.ModelViewSet):
    filter_class = ResultFilter
    serializer_class = ResultSerializer
    queryset = Result.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


