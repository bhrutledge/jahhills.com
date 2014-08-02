# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0009_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='credits',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='lyrics',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
