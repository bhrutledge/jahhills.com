# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0008_auto_20140802_0116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
