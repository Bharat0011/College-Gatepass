from django.db import models

# Create your models here.
class hod_data(models.Model):
    username=models.CharField(max_length=150)
    password=models.CharField(max_length=200)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=150)
    email=models.EmailField()
    mobile_no=models.BigIntegerField()