# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-03 23:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0003_auto_20180303_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='resource_type',
            new_name='resource_types',
        ),
    ]
