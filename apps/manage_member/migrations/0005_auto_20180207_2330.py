# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-07 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_member', '0004_auto_20180207_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='incarcerated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]