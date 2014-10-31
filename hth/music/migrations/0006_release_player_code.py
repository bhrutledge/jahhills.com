# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_video_preview_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='player_code',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
