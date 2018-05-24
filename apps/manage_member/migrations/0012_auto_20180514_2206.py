# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-15 03:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_member', '0011_auto_20180504_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='checked_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.CharField(blank=True, help_text="birthday in YYYYMMDD, if no full birthday, unknowns are '00'", max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='facility',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='update_release.Facility'),
        ),
        migrations.AlterField(
            model_name='member',
            name='given_name',
            field=models.CharField(blank=True, help_text='given name', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='given_name_alpha',
            field=models.CharField(blank=True, help_text='given name, last name first', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='typestate',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
