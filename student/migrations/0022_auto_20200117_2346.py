# Generated by Django 3.0 on 2020-01-17 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_email_verifiction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stu_signup',
            name='icard_img',
            field=models.ImageField(blank=True, null=True, upload_to='profile_img'),
        ),
        migrations.AlterField(
            model_name='stu_signup',
            name='user_img',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
    ]
