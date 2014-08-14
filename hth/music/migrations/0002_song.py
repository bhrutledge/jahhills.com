# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('credits', models.TextField(blank=True)),
                ('lyrics', models.TextField(blank=True)),
                ('track', models.PositiveIntegerField(blank=True, null=True)),
                ('release', models.ForeignKey(null=True, blank=True, to='music.Release')),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
    ]
