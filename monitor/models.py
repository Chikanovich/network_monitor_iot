from django.db import models

# Create your models here.


class NetworkUsage(models.Model):
    date_created = models.DateTimeField('date created')
    ip_address = models.GenericIPAddressField('ip address')
    vendor = models.CharField(max_length=200)
