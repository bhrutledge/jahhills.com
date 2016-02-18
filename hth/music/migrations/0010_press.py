# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 01:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_auto_20160215_0146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Press',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish', models.BooleanField(default=False, help_text="Sets 'publish on' to now unless already set.")),
                ('publish_on', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('source_url', models.URLField(blank=True)),
                ('body', models.TextField(blank=True)),
                ('quote', models.BooleanField(default=True)),
                ('release', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Release')),
            ],
            options={
                'verbose_name_plural': 'press',
                'ordering': ['-date'],
            },
        ),
    ]
