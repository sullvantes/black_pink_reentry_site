# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re 
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required

from django.db.models import Max

from models import *

# Create your views here.

@login_required
def home(request):

    all_members = Member.objects.all().order_by('-checked_at')[:100]
    
    response = {
        'members' : all_members,
        }    
    return render(request, "manage_member/home.html",response)

@login_required
def add_members(request):
    if request.method=='POST':
        ids = request.POST['IDsToAdd'].replace(',','')
        list_of_ids = ids.split()
        for id in list_of_ids:
            id = re.sub('[^A-Z0-9]','', id.upper())
            # print id
            if (len(id) == 6 and id[1:].isdigit()) or (len(id) == 8 and id.isdigit()) :
                if Member.objects.filter(gov_id = id).count()<1:
                    Member.objects.create(gov_id = id, created_by=request.user)
    return redirect(reverse('members:home'))

@login_required
def show(request):
    all_members = Member.objects.all()
    
    response = {
        'result':all_members, 
        }    
    return render(request, "manage_member/all_members.html", response)

@login_required
def update_existing(request):
    response = {
        'result':request.session["idoc_result"], 
        }    
    return redirect(reverse('members:show'))

@login_required
def update_searched(request):
    if request.user.is_authenticated():
        username = request.user
        entry_values = ['incarcerated_date', 'parole_date','discharge_date' ]
        for entry in request.session["search_result"]:
            if entry['isValid'] == True:
            #     if Member.objects.get(gov_id=entry['gov_id']):
            #         this_member = Member.objects.get(gov_id = entry['gov_id'])
            #         for value in entry_values:
            #             try:
            #                 this_member.make_change(value, entry[value])
            #             except:
            #                 pass
            #     else:
            #         this_facility = Facility.objects.get(scraped_name=entry['facility_name'])
            #         new_member = Member(facility=this_facility,created_by=username)
            #         for key, value in entry.items():
            #             setattr(new_member, key, value)
            #         new_member.save()
            #         this_member=new_member
                entry_facility = Facility.objects.get(scraped_name = entry['facility_name'])
                print entry_facility
            # for key, value in entry.iteritems():
            #     print "\t%s : %s " % (key, value)

    response = {
        'result':request.session["search_result"], 
        }    
    return redirect(reverse('release:results'))