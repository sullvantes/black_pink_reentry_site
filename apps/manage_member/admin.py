# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

# Register your models here.

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [ 'gov_id', 'given_name','given_name_alpha', 'typestate', 'birthday', 'so', 'status', 'facility', 'created_by', 'created_at', 'updated_at']
    
@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ['member', 'incarcerated_date', 'parole_date', 'discharge_date', 'created_at']