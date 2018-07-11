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
    
    def __str__(self):
        return self.name

    
    def mailing_address(self):
        address = []
        if self.name:
            address.append(self.name.replace("Correctional Center", "CC"))
        else:
            address.append(self.scraped_name)
        address.append(self.street_address);
        city_state_zip = self.city + ", "+ self.state + " " + self.zip_code
        address.append(city_state_zip)                    
        return address
    
    def save(self,**kwargs):
        if kwargs.has_key('request') and self.user is None:
            request = kwargs.pop('request')
            self.created_by= request.user
        super(Facility, self).save(**kwargs)


class FacilityForm(forms.ModelForm,):
    class Meta:
        model = Facility
        fields = ['scraped_name', 'name', 'street_address', 'city', 'state', 'zip_code']
        widgets = { 
            'scraped_name': forms.TextInput(),
            'name': forms.TextInput(),
            'street_address': forms.TextInput(),
            'city': forms.TextInput(),
            'state': forms.TextInput(),
            'zip_code': forms.TextInput(),
        }
        verbose_name_plural = "facilities"
        ordering = ['state', 'name', '-general', 'address1']
        
    def save(self, commit=True ,*args, **kwargs):
        request = None
        if kwargs.has_key('request'):
            request = kwargs.pop('request')
        m = super(FacilityForm, self).save(commit=False, *args, **kwargs)
        if request is not None:
            m.created_by= request.user
            m.save()
    
#    def __init__(self, *args, **kwargs):
#        request = kwargs.pop('request')
#        self.created_by = request.user
#        super(FacilityForm, self).__init__(*args, **kwargs)
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


        