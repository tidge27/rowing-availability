# Generated by Django 2.1 on 2018-08-23 05:37

import availability_site.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_myuser_crsid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='crsid',
            field=availability_site.models.CharNullField(blank=True, default=None, max_length=64, null=True, unique=True),
        ),
    ]