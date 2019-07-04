# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('source_url', models.CharField(blank=True, max_length=200)),
                ('embed_code', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('credits', models.TextField(blank=True)),
                ('release', models.ForeignKey(to='music.Release', blank=True, null=True)),
            ],
            options={
                'ordering': ['publish', '-publish_on'],
            },
            bases=(models.Model,),
        ),
    ]
