# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-05 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_member', '0015_auto_20180705_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='msr',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='member',
            name='so',
            field=models.NullBooleanField(),
        ),
    ]
