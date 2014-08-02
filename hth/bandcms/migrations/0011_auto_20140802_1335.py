# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0010_auto_20140802_1332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ['title']},
        ),
    ]
