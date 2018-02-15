# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.forms import ModelForm
from ..main.models import *
from ..update_release.models import *


STATUS_CHOICES = (
    ('Inc', 'IN CUSTODY'),
    ('FREE', 'N/A'),
    ('Par', 'PAROLED'),
)

# Create your models here.
class Member(models.Model):
    gov_id=models.CharField(max_length=24, blank=False,help_text="Government issued ID")
    given_name = models.CharField(max_length=255, blank=True,help_text="given name")
    given_name_alpha = models.CharField(max_length=255, blank=True,help_text="given name, last name first")
    typestate=models.CharField(max_length=10, blank=True,help_text="given name, last name first")
    birthday=models.CharField(max_length = 10, blank=True,help_text="birthday in YYYYMMDD, if no full birthday, unknowns are '00'")
    
    
    so=models.NullBooleanField(null=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='Inc' )
    facility = models.ForeignKey(Facility, related_name = 'members')
    created_by = models.ForeignKey(User, related_name = 'members')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    
    def __str__(self):
        return self.given_name
        
class NewMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['gov_id']
        widgets = { 
            'gov_id': forms.TextInput(),
#            'number_street': forms.TextInput(),
#            'city': forms.TextInput(),
#            'state': forms.TextInput(),
#            'zip_code': forms.TextInput(),
        }
#        error_messages = {
#            NON_FIELD_ERRORS: {
#                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
#            }
#        }

class Release(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    incarcerated_date=models.DateTimeField(blank=True, null=True)
    parole_date=models.DateTimeField(blank=True, null=True)
    discharge_date=models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
