# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0013_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='credits',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='embed_code',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='release',
            field=models.ForeignKey(to='bandcms.Release', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='source_url',
            field=models.CharField(default='', max_length=200, blank=True),
            preserve_default=False,
        ),
    ]
