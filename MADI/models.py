from django.db import models

class config(models.Model):
    caseNo = models.CharField(max_length=200)
    dart = models.BooleanField(null=True)
    mod = models.BooleanField(null=True)