# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20140826_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='preview_url',
            field=models.URLField(blank=True, default='http://placehold.it/480x360&text=[preview]', help_text='A link to the preview image.'),
            preserve_default=False,
        ),
    ]
