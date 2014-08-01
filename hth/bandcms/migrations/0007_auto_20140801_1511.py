# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0006_auto_20140801_1501'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='release',
            options={'ordering': ['-date']},
        ),
    ]
