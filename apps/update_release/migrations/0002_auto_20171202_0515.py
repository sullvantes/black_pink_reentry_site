# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 05:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('update_release', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facility',
            old_name='number_street',
            new_name='street_address',
        ),
    ]
