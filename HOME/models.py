from django.db import models

class contact(models.Model):
    ID = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    body = models.CharField(max_length=500)