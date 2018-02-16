# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 23:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name for facility', max_length=255)),
                ('scraped_name', models.CharField(blank=True, help_text='Name for facility that is scraped from website', max_length=255)),
                ('number_street', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
                ('zip_code', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facilities', to='main.User')),
            ],
        ),
    ]