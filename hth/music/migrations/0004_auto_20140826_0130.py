# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='cover_url',
            field=models.URLField(blank=True, default='', help_text='A link to the cover art, at the highest desired resolution.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='release',
            name='publish',
            field=models.BooleanField(default=False, help_text="Sets 'publish on' to now unless already set."),
        ),
        migrations.AlterField(
            model_name='release',
            name='slug',
            field=models.SlugField(help_text='A unique label, used in URLs.', unique=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='publish',
            field=models.BooleanField(default=False, help_text="Sets 'publish on' to now unless already set."),
        ),
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(help_text='A unique label, used in URLs.', unique=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='track',
            field=models.PositiveIntegerField(null=True, blank=True, help_text="The track number on 'release'."),
        ),
        migrations.AlterField(
            model_name='video',
            name='publish',
            field=models.BooleanField(default=False, help_text="Sets 'publish on' to now unless already set."),
        ),
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(help_text='A unique label, used in URLs.', unique=True),
        ),
    ]
