from django.db import models

class config(models.Model):
    caseNo = models.CharField(max_length=200)
    ERFpath = models.CharField(max_length=200)
    dart = models.BooleanField(null=True)
    mod = models.BooleanField(null=True)

class IRFdata(models.Model):
    CN = models.CharField(max_length=200)
    tail = models.CharField(max_length=200)
    IRFTitle = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    affected = models.CharField(max_length=200)
    IRFNo = models.CharField(max_length=200)
    ROED = models.BooleanField(null=True)
    dart = models.BooleanField(null=True)
    mod = models.BooleanField(null=True)
    fileName = models.CharField(max_length=200, default='')