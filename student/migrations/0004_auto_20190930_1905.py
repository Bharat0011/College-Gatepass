# Generated by Django 2.2.5 on 2019-09-30 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='in_req',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_time', models.DateTimeField()),
                ('reason', models.CharField(max_length=20)),
                ('reason_des', models.TextField()),
                ('username', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_no', models.BigIntegerField()),
                ('req_accept_time', models.DateTimeField()),
                ('in_time', models.DateTimeField()),
                ('status', models.CharField(max_length=150)),
            ],
        ),
        migrations.DeleteModel(
            name='img',
        ),
    ]