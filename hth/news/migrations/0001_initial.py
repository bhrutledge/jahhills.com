# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
    ]
