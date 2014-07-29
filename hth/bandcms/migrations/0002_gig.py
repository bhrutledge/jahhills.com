# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=True)),
                ('publish_on', models.DateTimeField(null=True, blank=True)),
                ('date', models.DateField()),
                ('venue', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
