# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#for pdfs
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
import sys, csv, string

from search_address import Places

def home(request):
    request.session['nearby_locations']={}
    return render(request, "housing/home.html")

def search(request):
    if request.method !="POST":
        return redirect(reverse('housing:home'))
    
    search_address = request.POST['address_string']
    search_address_obj = Places(search_address)
    try:
        request.session['search_address']= search_address_obj.full_address
        print request.session['search_address']
    except:
        request.session['search_address']= search_address
    request.session['nearby_locations']=search_address_obj.restrictive_locations()
    print request.session['nearby_locations']
    request.session['valid_address']=search_address_obj.valid_address
    return redirect(reverse('housing:results'))

def results(request):
    response = {
        'search_address':request.session['search_address'],
        'nearby_locations':request.session['nearby_locations']
        }    
    return render(request, "housing/results.html", response)

#     if request.session['new_search']:
#         search_result=[]
#         for raw_id in request.session['search_members']:
#             id = re.sub('[^A-Z0-9]','', raw_id.upper())
#             if id.isdigit():
#                 id=id.zfill(8)
#                 memb = Fed_Member(id).return_dict()
#                 try:
#                     memb['bday_abb'] = "~" + memb['birthday'][0:4]
#                 except:
#                     memb['bday_abb']=""
#             else:
#                 memb=Ill_Member(id).return_dict()
#                 try:
#                     memb['bday_abb'] = memb['birthday'][0:4]+'/'+memb['birthday'][4:2]+'/'+memb['birthday'][6:2]
#                 except:
#                     memb['bday_abb']=""    
#             try:
#                 memb_fac = Facility.objects.get(scraped_name = memb['facility_name'])
#                 memb['mailing_address']=memb_fac.mailing_address()
#             except:
#                 memb['mailing_address']=[[],[],[]]
#             search_result.append(memb)
            
#         request.session["search_result"]=search_result
        
# #        for obj in request.session["search_objects"]:
# #            print 1
#         request.session["new_search"]=False
    response = {
        'result':{}, 
        }    
    return render(request, "housing/results.html", response)
