# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['scraped_name', 'name','street_address', 'city', 'state', 'zip_code', 'created_by', 'mailing_address']




