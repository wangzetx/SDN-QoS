from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 32)
    password = models.CharField(max_length = 32)

class Flow(models.Model):   
    id = models.AutoField(primary_key = True)
    basic = models.TextField()
    match = models.TextField()
    instructions = models.TextField(null = True)
    statistics = models.TextField(null = True)

class Meter(models.Model):
    id = models.AutoField(primary_key = True)
    # content = models.TextField(null = True)
    basic = models.TextField(null = True)
    meterBandHeaders = models.TextField(null = True)
    meterStatistics = models.TextField(null = True)
