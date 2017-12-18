# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User



# Create your models here.
class Facility(models.Model):
    name = models.CharField(max_length=255, blank=True,help_text="Name for facility")
    scraped_name = models.CharField(max_length=255, blank=True,
        help_text="Name for facility that is scraped from website")
    street_address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zip_code = models.TextField()
    created_by = models.ForeignKey(User, related_name = 'facilities')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 

    
    def mailing_address(self):
        address = []
        address.append(self.scraped_name);
        address.append(self.street_address);
        city_state_zip = self.city + ", "+ self.state + " " + self.zip_code
        address.append(city_state_zip)                    
        return address


class FacilityForm(forms.ModelForm):
    class Meta:
        model=Facility
        fields = ['scraped_name', 'number_street', 'city', 'state', 'zip_code']
        widgets = { 
            'scraped_name': forms.TextInput(),
            'number_street': forms.TextInput(),
            'city': forms.TextInput(),
            'state': forms.TextInput(),
            'zip_code': forms.TextInput(),
        }
    
#    phone = PhoneNumberField(blank=True, max_length=255)
#    general = models.BooleanField(default=False,
#        help_text="Is this address a 'general mail' address for facilities with this code?")
#    type = models.ForeignKey(FacilityType, null=True, blank=True)
#    administrator = models.ForeignKey(FacilityAdministrator, null=True, blank=True)
#    operator = models.ForeignKey(FacilityOperator, null=True, blank=True)

#    provenance = models.CharField(max_length=255, verbose_name="data source")
#    provenance_url = models.CharField(max_length=255, verbose_name="data source URL")

#    chapters = models.ManyToManyField('blackandpink.Chapter', blank=True)
#    legacy_zoho = JSONField(blank=True, null=True)

#    objects = FacilityManager()

    
    class Meta:
        verbose_name_plural = "facilities"
        ordering = ['state', 'name', '-general', 'address1']
