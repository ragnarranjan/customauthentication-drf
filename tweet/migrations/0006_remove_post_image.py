# Generated by Django 3.2.7 on 2021-09-23 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0005_auto_20210923_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]