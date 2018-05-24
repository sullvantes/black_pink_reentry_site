# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

# Register your models here.

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    fields = ('name', 'resource_types', 'dedicated_to', 'address', 'city', 'state', 'zip_code', 'county', 'phone', 'contact_name', 'email', 'website', 'notes', 'restrictions', 'bp_contact', 'bp_supported_note', 'created_by')
    list_display = ['name', 'get_types', 'dedicated_to', 'address', 'city', 'state', 'zip_code', 'county', 'phone', 'contact_name', 'email', 'website', 'notes', 'restrictions', 'bp_contact', 'bp_supported_note', 'created_by']

    def get_types(self, obj):
        return "\n".join([t.name for t in obj.resource_types.all()])

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']