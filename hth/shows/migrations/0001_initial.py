# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(blank=True, null=True)),
                ('date', models.DateField()),
                ('venue', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('details', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
    ]
