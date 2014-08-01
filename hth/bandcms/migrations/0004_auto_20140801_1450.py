# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bandcms', '0003_auto_20140724_1116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gig',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='gig',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='gig',
            name='details',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]
