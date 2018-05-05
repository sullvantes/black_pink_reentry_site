# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-05 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0007_auto_20180504_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='resource_types',
            field=models.ManyToManyField(blank=True, related_name='resources', to='resources.ResourceType', verbose_name='Type'),
        ),
    ]
