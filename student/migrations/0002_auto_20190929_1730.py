# Generated by Django 2.2.5 on 2019-09-29 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stu_signup',
            name='icard_img',
            field=models.ImageField(upload_to='profile_img/'),
        ),
        migrations.AlterField(
            model_name='stu_signup',
            name='user_img',
            field=models.ImageField(upload_to='profile/'),
        ),
    ]