# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class ResourceType(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, related_name = 'resource_types')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    
    def __str__(self):      
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=255)
    resource_types=models.ManyToManyField(ResourceType, related_name = 'resources', verbose_name = 'Type', blank=True)
    dedicated_to=models.TextField(null=True, blank=True)
    address=models.CharField(max_length = 255, null = True, blank= True)
    city=models.CharField(max_length = 55, null = True, blank= True)
    state=models.CharField(max_length = 2, null = True, blank= True)
    zip_code=models.CharField(max_length = 5,null=True, blank= True)
    county=models.CharField(max_length = 255, null = True, blank= True)
    phone = models.CharField(max_length = 255, null = True, blank= True)
    contact_name = models.CharField(max_length = 255, null=True, blank= True)
    email = models.CharField(max_length=255,null=True, blank= True)
    website = models.URLField(null=True, blank= True)
    notes=models.TextField(null=True, blank= True)
    restrictions=models.TextField(null=True, blank= True)
    bp_contact = models.CharField(max_length = 255, null = True, blank= True)
    bp_supported_note =models.TextField(null=True, blank= True)
    created_by = models.ForeignKey(User, related_name = 'created_resources', blank = True)
    submitted_by = models.CharField(max_length = 255, null = True, blank= True)
    approved = models.BooleanField(default = True)
    approved_by = models.ForeignKey(User, related_name = 'approved_resources', null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 

    def __str__(self):
        return self.name
    
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['resource_types', 'name', 'dedicated_to', 'address', 'city', 'state', 'zip_code', 'county', 'phone',  'contact_name', 'email', 'website', 'notes', 'restrictions', 'bp_contact', 'bp_supported_note', 'created_by', 'submitted_by']
        widgets = {
            'resource_types': forms.CheckboxSelectMultiple(),
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
            'notes': forms.Textarea(attrs={'placeholder': 'Please enter public notes for an individual considering this resource.'}),
            'restrictions': forms.Textarea(attrs={'placeholder': 'Restrictions A Member Should Know About'}),
            'bp_contact': forms.TextInput(attrs={'placeholder': 'B&P Member Contact'}),
            'bp_supported_note': forms.Textarea(attrs={'placeholder': 'Write in here how supportive this resource is of Black and Pink Fam and Values'}),
            }

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['resource_types'].widget.attrs.update({
                'class': 'form-check form-check-inline'
            })