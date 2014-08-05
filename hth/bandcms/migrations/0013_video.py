# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0012_auto_20140803_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('publish', models.BooleanField(default=False)),
                ('publish_on', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
