# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-04 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0005_auto_20180504_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='dedicated_to',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_types',
            field=models.ManyToManyField(related_name='resources', to='resources.ResourceType', verbose_name='Type'),
        ),
    ]
