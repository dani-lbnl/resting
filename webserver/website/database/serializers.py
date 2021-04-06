
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

from database.models import Source

class SourceSerializer(serializers.HyperlinkedModelSerializer):

    results = serializers.HyperlinkedRelatedField(many=True,view_name='result-detail',read_only=True)

    test_results = serializers.HyperlinkedRelatedField(many=True,view_name='result-detail',read_only=True)

    class Meta:
        model = Source
        fields = ['id', 'patientid', 'offset', 'sex', 'age', 'finding', 'RT_PCR_positive', 'survival', 'intubated', 'intubation_present', 'went_icu', 'in_icu', 'needed_supplemental_O2', 'extubated', 'temperature', 'pO2_saturation', 'leukocyte_count', 'neutrophil_count', 'lymphocyte_count', 'view', 'modality', 'date', 'location', 'folder', 'filename', 'doi', 'url', 'license', 'clinical_notes', 'other_notes', 'thumbnail_folder', 'thumbnail_filename', 'artifacts_and_distortion', 'notes', 'thumbnail_filename_wildcard', 'results', 'test_results']

from database.models import Result

class ResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Result
        fields = ['id', 'directory', 'filename', 'method', 'source', 'test_sources']


