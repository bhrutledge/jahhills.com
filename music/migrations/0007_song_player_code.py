# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_release_player_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='player_code',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
