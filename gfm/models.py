from django.db import models

# Create your models here.
class gfm_signup(models.Model):
    gfm=models.CharField(max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField()
    mobile_no=models.BigIntegerField()
    icard_no=models.BigIntegerField()
    password=models.CharField(max_length=100)
    valid=models.CharField(max_length=8)
