# Generated by Django 2.1 on 2018-08-23 05:10

import availability_site.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180822_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='crsid',
            field=availability_site.models.CharNullField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]