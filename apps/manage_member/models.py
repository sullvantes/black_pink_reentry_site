# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from ..update_release.models import *


STATUS_CHOICES = (
    ('Inc', 'IN CUSTODY'),
    ('FREE', 'N/A'),
    ('Par', 'PAROLED'),
    ('UNK', 'Unknown'),
)


# Create your models here.
class Member(models.Model):
    gov_id=models.CharField(max_length=24, blank=False,help_text="Government issued ID")
    first_name = models.CharField(max_length=255, blank=True,help_text="first name", null = True)
    last_name = models.CharField(max_length=255, blank=True,help_text="last name", null = True)
    typestate=models.CharField(max_length=10, blank=True, null = True)
    # birthday=models.CharField(max_length = 10, blank=True, null = True, help_text="birthday in YYYYMMDD, if no full birthday, unknowns are '00'")
    birth_date=models.DateField(blank=True, null=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='Inc' )
    facility = models.ForeignKey(Facility, related_name = 'members', null = True )
    incarcerated_date=models.DateField(blank=True, null=True)
    parole_date=models.DateField(blank=True, null=True)
    discharge_date=models.DateField(blank=True, null=True)
    so=models.BooleanField(blank=True, default=False)
    msr=models.BooleanField(blank=True, default=False)
    life=models.BooleanField(blank=True, default=False)
    created_by = models.ForeignKey(User, related_name = 'members')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    
    
    def __str__(self):
        return self.last_name+ ', '+self.first_name
    
    def make_change(self, attr, new_value):
        old_value = getattr(self, attr)
        if old_value is not new_value:
            setattr(self, attr, new_value)
            self.save()
            change_str = attr+" was changed from "+str(old_value)+" to "+str(new_value)
            return Change.objects.create(member = self, attribute = attr, verbose= change_str)
        else:
            return None
        
    def alpha_name(self):
        return "%s, %s" % (self.last_name, self.first_name)
    
    def mailing_address(self):
        address=[]
        first_line = self.first_name, self.last_name, self.gov_id
        address.append(first_line)
        for line in self.facility.mailing_address():
            address.append(line)
        return address
    # def earliest_date(self):
    #     if self.parole_date:
    #         return self.parole_date
    #     else:
    #         return self.discharge_date
            
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

class Change(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    attribute = models.CharField(max_length=255, blank=True,help_text="attribute changed")
    verbose = models.CharField(max_length=255, blank=True,help_text="verbose change")
    created_at = models.DateTimeField(auto_now_add = True)

    