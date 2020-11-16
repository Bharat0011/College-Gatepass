from django.db import models

# Create your models here.
class stu_signup(models.Model):
    valid=models.CharField(max_length=8)
    username=models.CharField(max_length=100)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    gender=models.CharField(max_length=20)
    password=models.CharField(max_length=200)
    email=models.EmailField()
    mobile_no=models.BigIntegerField()
    year=models.CharField(max_length=2)
    branch=models.CharField(max_length=100)
    roll_no=models.IntegerField()
    gfm=models.CharField(max_length=200)
    icard_img=models.TextField(null=True, blank=True)
    # user_img=models.ImageField(upload_to='profile',null=True, blank=True)
    user_img=models.TextField(null=True, blank=True)
    otp = models.CharField(max_length=50)
    email_verify = models.CharField(max_length=10)
    email_otp = models.CharField(max_length=10)


class in_req(models.Model):
    apply_time=models.DateTimeField()
    reason=models.CharField(max_length=20)
    request_type=models.CharField(max_length=100)
    reason_des=models.TextField()
    username=models.CharField(max_length=200)
    gmail=models.EmailField()
    mobile_no=models.BigIntegerField()
    req_accept_time=models.DateTimeField(null=True, blank=True)
    in_time=models.DateTimeField(null=True, blank=True)
    out_time=models.DateTimeField(null=True, blank=True)
    in_req_count=models.IntegerField(default=0)
    out_req_count=models.IntegerField(default=0)
    req_date=models.DateField()
    status=models.CharField(max_length=150)   #accepted/rejected/in/out
    year=models.CharField(max_length=2)
    branch=models.CharField(max_length=100)
    req_acceped_by = models.CharField(max_length=320)
    first_name=models.CharField(max_length=200,default='a')
    last_name=models.CharField(max_length=200 ,default='a')


class email_verifiction(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=60)