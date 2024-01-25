from django.db import models

# Custom Registration

class MyRegistrations(models.Model):
    name        = models.CharField(max_length=100)
    email       = models.CharField(max_length=255)
    password    = models.CharField(max_length=255)
    phone       = models.CharField(max_length=255)
    city        = models.CharField(max_length=100)
    role        = models.CharField(max_length=100)

