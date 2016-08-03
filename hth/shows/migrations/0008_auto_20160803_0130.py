# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-03 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0007_remove_gig_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='address',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='venue',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='venue',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
