# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-12 23:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_member', '0006_release_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='incarcerated_date',
        ),
        migrations.AddField(
            model_name='release',
            name='incarcerated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='release',
            name='discharge_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='release',
            name='parole_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
