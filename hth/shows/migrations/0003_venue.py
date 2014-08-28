# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0002_auto_20140826_2342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('website', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
