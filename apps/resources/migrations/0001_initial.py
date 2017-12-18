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
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dedicated_to', models.TextField(null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=55, null=True)),
                ('state', models.CharField(max_length=2, null=True)),
                ('zip_code', models.CharField(max_length=5, null=True)),
                ('county', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=255, null=True)),
                ('contact_name', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('website', models.URLField(null=True)),
                ('notes', models.TextField(null=True)),
                ('restrictions', models.TextField(null=True)),
                ('bp_contact', models.CharField(max_length=255, null=True)),
                ('bp_supported_note', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='main.User')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_types', to='main.User')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.ManyToManyField(to='resources.OrganizationType'),
        ),
    ]
