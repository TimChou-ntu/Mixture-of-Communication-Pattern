from django.db import models

# Create your models here.

class FibReqItem(models.Model):
    order = models.PositiveIntegerField()

class FibResItem(models.Model):
    order = models.PositiveIntegerField()
    value = models.PositiveIntegerField()