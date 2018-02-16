# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-15 21:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_member', '0007_auto_20180212_2301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Change',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.CharField(blank=True, help_text='verbose change', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='release',
            name='member',
        ),
        migrations.AddField(
            model_name='member',
            name='discharge_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='incarcerated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='parole_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Release',
        ),
        migrations.AddField(
            model_name='change',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manage_member.Member'),
        ),
    ]