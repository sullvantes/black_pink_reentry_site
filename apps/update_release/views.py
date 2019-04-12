# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

#for pdfs
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from ..update_release.models import *
import sys, csv, string

from IL_release import *
from FED_release import *


def home(request):
    return render(request, "update_release/home.html")

def ind_search(request):
    if request.method !="POST":
        return redirect(reverse('release:home')) 
    id_string=request.POST['govID'].replace(',','')
    allIds = id_string.split()
    
    request.session['search_member'] =[]
    
    request.session['search_members'] = allIds
    request.session['new_search']=True
    return redirect(reverse('release:results'))

def results(request):
    if request.session['new_search']:
        search_result=[]
        for raw_id in request.session['search_members']:
            id = re.sub('[^A-Z0-9]','', raw_id.upper())
            if id.isdigit():
                id=id.zfill(8)
                memb = Fed_Member(id).return_dict()
                try:
                    memb['bday_abb'] = "~" + memb['birthday'][0:4]
                except:
                    memb['bday_abb']=""
            else:
                illmemb=Ill_Member(id)
                memb=illmemb.return_dict()
                try:
                    memb['bday_abb'] = memb['birthday'][0:4]+'/'+memb['birthday'][4:2]+'/'+memb['birthday'][6:2]
                except:
                    memb['bday_abb']=""    
            try:
                memb_fac = Facility.objects.get(scraped_name = memb['facility_name'])
                memb['mailing_address']=memb_fac.mailing_address()
            except:
                memb['mailing_address']=[[],[],[]]
            search_result.append(memb)
            
        request.session["search_result"]=search_result
        request.session["new_search"]=False
    response = {
        'result':request.session["search_result"], 
        }    
    return render(request, "update_release/results.html", response)

def results_hidden(request):
    response = {
        'result':request.session["search_result"], 
        }    
    return render(request, "update_release/results_hidden.html", response)

def add_facility(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect(reverse ('release:new_facility'),)

    # if not POST, create a blank form
    return redirect(reverse('release:new_facility'))

def new_facility(request):
    form=FacilityForm()
    return render(request,"update_release/new_facility.html",{'form': form})

def all_facilities(request):
    all_facilities = Facility.objects.all().order_by('scraped_name')
    return render(request, "update_release/all_facilities.html",{'all_facilities':all_facilities})

def facility_home(request,facility_id):
    instance= Facility.objects.get(id=facility_id)
    form=FacilityForm(instance=instance)
    return render(request,"update_release/facility_home.html",{'form': form})

    
def pdf_print(request):
   # Create the HttpResponse object with the appropriate PDF headers.
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="Mailing Labels.pdf"'

   # Create the PDF object, using the response object as its "file."
   p = canvas.Canvas(response)

   # Draw things on the PDF. Here's where the PDF generation happens.
   # See the ReportLab documentation for the full list of functionality.
   p.drawString(100, 100, "Hello world.")

   # Close the PDF object cleanly, and we're done.
   p.showPage()
   p.save()
   return response

def csv_print(request):
    # Create the HttpResponse object with the appropriate CSV header.

    timestr = time.strftime("%Y%m%d_%H%M%S")
    filename="Updated_Release"+timestr+".csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+filename

    fieldnames = [  'ID', 
                    'Name', 
                    'Location',
                    'Address',
                    'Projected Parole Date',
                    'Projected Discharge Date',
                    'Incarcerated Date',
                    'Birthday',
                    'Registry?'
                 ]
    writer = csv.DictWriter(response, dialect='excel', fieldnames=fieldnames, extrasaction='ignore')
    csv_list=[]
    for memb in request.session['search_result']:
        new_dict = {}
        try:
            mailing_address = '%s %s %s\n' % (memb['first_name'], memb['last_name'], memb['gov_id'])
            mailing_address += '\n'.join(memb['mailing_address']).replace('NA,', '').replace('NA','')
        except:
            mailing_address = "Facility is not in the DB. Please Investigate."
        new_dict['Address'] = mailing_address
        print new_dict['Address']
        try:
            new_dict['Name']=memb['first_name'] + ' ' + memb["last_name"]
        except:
            pass
        new_dict['ID']=memb['gov_id']
        new_dict['Location']=memb['facility_name']
        
        try:
            new_dict['Projected Parole Date']=memb['parole_date']
        except:
            pass
        try:
            new_dict['Projected Discharge Date']=memb['discharge_date']
        except:
            pass
        try:
            if memb['typestate'] == 'FED':
                new_dict['Birthday']=memb['bday_abb']
            else:
                new_dict['Birthday']=memb['birthday']
        except:
            pass
        try:
            new_dict['Registry?']=memb['so']
        except:
            pass
        print new_dict
        csv_list.append(new_dict)
            
    writer.writeheader()
    for memb in csv_list:
        writer.writerow(memb)

    return response
