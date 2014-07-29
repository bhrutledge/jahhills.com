# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0002_gig'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gig',
            name='details',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
