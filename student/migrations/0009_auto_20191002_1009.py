# Generated by Django 2.2.5 on 2019-10-02 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20191001_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stu_signup',
            name='icard_img',
            field=models.ImageField(upload_to='profile_img'),
        ),
        migrations.AlterField(
            model_name='stu_signup',
            name='user_img',
            field=models.ImageField(upload_to='profile'),
        ),
    ]
