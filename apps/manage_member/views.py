# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.timezone import make_aware

from django.db.models import Max

from models import *

# Create your views here.

def home(request):
    all_members = Member.objects.all()
    
    response = {
        }    
    return render(request, "resources/home.html",response)

def add(request):
    response = {
        'result':request.session["idoc_result"], 
        }    
    return render(request, "manage_member/add.html", response)
    
def show(request):
#    all_members = Member.objects.all().annotate(Max(''))
#    hottest_cake_ids = Bakery.objects.annotate(hottest_cake_id=max('cake__id')).values_list('hottest_cak‌​e_id', flat=True)
#    hottest_cakes = Cake.objects.filter(id__in=hottest_cake_ids)
#    
    
#    latest_release_ids = Member.objects.annotate(latest_release_id=max('release__id')).values_list('latest_release_id', flat=True)
#    latest_releases = Release.objects.filter(id__in=latest_release_ids)
#    
#    all_members = Member.objects.all()
    all_members = Member.objects.annotate(newest_entry = Max('release__created_at'))
    
    response = {
        'result':all_members, 
        }    
    return render(request, "manage_member/all_members.html", response)

def update_existing(request):
    response = {
        'result':request.session["idoc_result"], 
        }    
    return redirect(reverse('members:show'))

def update_searched(request):
    if request.user.is_authenticated():
        username = request.user
        entry_values = ['incarcerated_date', 'parole_date','discharge_date' ]
        for entry in request.session["search_result"]:
            if entry['isValid'] == True:
                if Member.objects.filter(gov_id=entry['gov_id']):
                    this_member = Member.objects.get(gov_id = entry['gov_id'])
                    for value in entry_values:
                        try:
                            this_member.make_change(value, entry[value])
                        except:
                            pass
                else:
                    this_facility = Facility.objects.get(scraped_name=entry['facility_name'])
                    new_member = Member(facility=this_facility,created_by=username)
                    for key, value in entry.items():
                        setattr(new_member, key, value)
                    new_member.save()
                    this_member=new_member
    response = {
        'result':request.session["search_result"], 
        }    
    return redirect(reverse('release:results'))