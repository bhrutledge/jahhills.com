# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0011_auto_20140802_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='release',
            field=models.ForeignKey(null=True, blank=True, to='bandcms.Release'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='track',
            field=models.PositiveIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
