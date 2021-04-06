
from django.db import models
from django.contrib.auth.models import User

class Source(models.Model):
    patientid = models.CharField(max_length=256,blank=True)
    offset = models.IntegerField(null=True,blank=True)
    sex = models.CharField(max_length=256,blank=True)
    age = models.IntegerField(null=True,blank=True)
    finding = models.CharField(max_length=256,blank=True)
    RT_PCR_positive = models.CharField(max_length=256,blank=True)
    survival = models.CharField(max_length=256,blank=True)
    intubated = models.CharField(max_length=256,blank=True)
    intubation_present = models.CharField(max_length=256,blank=True)
    went_icu = models.CharField(max_length=256,blank=True)
    in_icu = models.CharField(max_length=256,blank=True)
    needed_supplemental_O2 = models.CharField(max_length=256,blank=True)
    extubated = models.CharField(max_length=256,blank=True)
    temperature = models.FloatField(null=True,blank=True)
    pO2_saturation = models.FloatField(null=True,blank=True)
    leukocyte_count = models.FloatField(null=True,blank=True)
    neutrophil_count = models.FloatField(null=True,blank=True)
    lymphocyte_count = models.FloatField(null=True,blank=True)
    view = models.CharField(max_length=256,blank=True)
    modality = models.CharField(max_length=256,blank=True)
    date = models.CharField(max_length=256,blank=True)
    location = models.CharField(max_length=256,blank=True)
    folder = models.CharField(max_length=256,blank=True)
    filename = models.CharField(max_length=256,blank=True)
    doi = models.CharField(max_length=256,blank=True)
    url = models.CharField(max_length=256,blank=True)
    license = models.CharField(max_length=256,blank=True)
    clinical_notes = models.CharField(max_length=256,blank=True)
    other_notes = models.CharField(max_length=256,blank=True)
    creator = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)

class Result(models.Model):
    directory = models.CharField(max_length=256,blank=True)
    filename = models.CharField(max_length=256,blank=True)
    method = models.CharField(max_length=256,blank=True)
    source = models.ForeignKey(Source,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)


