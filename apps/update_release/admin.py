# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

#class AlternateNameInline(admin.StackedInline):
#    model = AlternateName
#    readonly_fields = ['name']
#    extra = 0
#    max_num = 0

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['scraped_name', 'street_address', 'city', 'state', 'zip_code', 'created_by', 'mailing_address']
#    list_filter = ['general', 'administrator', 'operator', 'state', 'type']
#    search_fields = ['code', 'name', 'address1', 'address2', 'city', 'state', 'zip']
#    #readonly_fields = ['code', 'name', 'city', 'address1', 'address2', 'state', 'zip', 'phone', 'general', 'type', 'administrator', 'operator', 'provenance', 'provenance_url']
#    inlines = [AlternateNameInline]

#@admin.register(FacilityAdministrator)
#class FacilityAdministratorAdmin(admin.ModelAdmin):
#    search_fields = ['name']
#    #readonly_fields = ['name']
#
#@admin.register(FacilityOperator)
#class FacilityOperatorAdmin(admin.ModelAdmin):
#    search_fields = ['name']
#    #readonly_fields = ['name']
#
#@admin.register(FacilityType)
#class FacilityTypeAdmin(admin.ModelAdmin):
#    search_fields = ['name']
#    #readonly_fields = ['name']
