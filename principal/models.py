from django.db import models

# Create your models here.
class principal_data(models.Model):
    username=models.CharField(max_length=150)
    password=models.CharField(max_length=200)