# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-22 22:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('update_release', '0003_auto_20171202_0557'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gov_id', models.CharField(help_text='Government issued ID', max_length=24)),
                ('given_name', models.CharField(blank=True, help_text='given name', max_length=255)),
                ('given_name_alpha', models.CharField(blank=True, help_text='given name, last name first', max_length=255)),
                ('birthday', models.DateTimeField(blank=True)),
                ('incarcerated_date', models.DateTimeField(blank=True)),
                ('parole_date', models.DateTimeField(blank=True)),
                ('discharge_date', models.DateTimeField(blank=True)),
                ('so', models.NullBooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to=settings.AUTH_USER_MODEL)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='update_release.Facility')),
            ],
        ),
    ]