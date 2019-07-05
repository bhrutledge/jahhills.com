# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='description',
            field=models.TextField(help_text='Type of gig, band line-up, video links, etc.', blank=True),
        ),
        migrations.AlterField(
            model_name='gig',
            name='details',
            field=models.TextField(help_text='Start time, cost, ticket and venue links, etc.', blank=True),
        ),
        migrations.AlterField(
            model_name='gig',
            name='publish',
            field=models.BooleanField(help_text="Sets 'publish on' to now unless already set.", default=False),
        ),
        migrations.AlterField(
            model_name='gig',
            name='slug',
            field=models.SlugField(help_text='A unique label, used in URLs.', unique=True),
        ),
    ]
