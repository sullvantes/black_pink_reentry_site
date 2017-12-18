# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.forms import ModelForm
from ..main.models import *


class OrganizationType(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, related_name = 'org_types')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    def __str__(self):      
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=255)
    org_type=models.ManyToManyField(OrganizationType)
    dedicated_to=models.TextField(null=True)
    address=models.CharField(max_length = 255, null = True)
    city=models.CharField(max_length = 55, null = True)
    state=models.CharField(max_length = 2, null = True)
    zip_code=models.CharField(max_length = 5,null=True)
    county=models.CharField(max_length = 255, null = True)
    phone = models.CharField(max_length = 255, null = True)
    contact_name = models.CharField(max_length = 255, null=True)
    email = models.CharField(max_length=255,null=True)
    website = models.URLField(null=True)
    notes=models.TextField(null=True)
    restrictions=models.TextField(null=True)
    bp_contact = models.CharField(max_length = 255, null = True)
    bp_supported_note =models.TextField(null=True)
    created_by = models.ForeignKey(User, related_name = 'resources')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['org_type', 'name', 'dedicated_to', 'address', 'city', 'state', 'zip_code', 'county', 'phone',  'contact_name', 'email', 'website', 'notes', 'restrictions', 'bp_contact', 'bp_supported_note']
        widgets = {
            'org_type': forms.CheckboxSelectMultiple(attrs={'id': 'inlineCheckbox', 'display':'inline'}),
            'name': forms.TextInput(),
            'dedicated_to': forms.TextInput(attrs={}),
            'address': forms.TextInput(attrs={}),
            'city': forms.TextInput(attrs={}),
            'state': forms.TextInput(attrs={}),
            'zip_code': forms.TextInput(attrs={}),
            'county': forms.TextInput(attrs={}),
            'phone': forms.TextInput(attrs={}),
            'contact_name': forms.TextInput(attrs={}),
            'email': forms.TextInput(attrs={}),
            'website': forms.TextInput(attrs={}),
            'notes': forms.Textarea(attrs={'placeholder': 'Please enter public notes for an individual considering this org.'}),
            'restrictions': forms.Textarea(attrs={'placeholder': 'Restrictions A Member Should Know About'}),
            'bp_contact': forms.TextInput(attrs={'placeholder': 'B&P Member Contact'}),
            'bp_supported_note': forms.Textarea(attrs={'placeholder': 'Write in here how supportive this org is of Black and Pink Fam and Values'}),
            }
