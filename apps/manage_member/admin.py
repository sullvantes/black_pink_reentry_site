# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

# Register your models here.

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('gov_id', 'first_name', 'last_name','typestate', 'birth_date', 'status', 'facility', 'incarcerated_date', 'parole_date', 'discharge_date', 'created_by', 'created_at', 'updated_at')
    search_fields = ['gov_id', 'first_name', 'last_name','typestate', 'status', 'created_by']


@admin.register(Change)
class ChangeAdmin(admin.ModelAdmin):
    list_display = ['member', 'attribute', 'verbose', 'created_at']