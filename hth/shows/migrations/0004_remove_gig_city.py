# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0003_venue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gig',
            name='city',
        ),
    ]
