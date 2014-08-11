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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(null=True, blank=True)),
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
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['publish', '-publish_on'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('credits', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('credits', models.TextField(blank=True)),
                ('lyrics', models.TextField(blank=True)),
                ('track', models.PositiveIntegerField(null=True, blank=True)),
                ('release', models.ForeignKey(to='bandcms.Release', null=True, blank=True)),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('source_url', models.CharField(max_length=200, blank=True)),
                ('embed_code', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('credits', models.TextField(blank=True)),
                ('release', models.ForeignKey(to='bandcms.Release', null=True, blank=True)),
            ],
            options={
                'ordering': ['publish', '-publish_on'],
            },
            bases=(models.Model,),
        ),
    ]
