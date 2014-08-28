# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0004_remove_gig_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='venue',
            field=models.ForeignKey(to='shows.Venue'),
        ),
    ]
