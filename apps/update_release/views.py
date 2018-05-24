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
                memb=Ill_Member(id).return_dict()
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
        
#        for obj in request.session["search_objects"]:
#            print 1
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
    
    writer = csv.writer(response,dialect='excel')
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
#    csv_dict= sorted(request.session['search_result'], key=lambda k: k[u'Alpha_Name']) 
    csv_dict=request.session['search_result']
    for dict in csv_dict:
        mailing_address=''
        try:
            for x in dict['mailing_address']:
                mailing_address+=(x.encode()+'\n')
        except:
            mailing_address = "Facility is not in the DB. Please Investigate."
        dict['Address'] = mailing_address
        try:
            dict['Name']=dict['given_name_alpha']
        except:
            pass
        dict['ID']=dict['gov_id']
        dict['Location']=dict['facility_name']
        
        try:
            dict['Projected Parole Date']=dict['parole_date']
        except:
            pass
        try:
            dict['Projected Discharge Date']=dict['discharge_date']
        except:
            pass
        try:
            if dict['typestate'] == 'FED':
                dict['Birthday']=dict['bday_abb']
            else:
                dict['Birthday']=dict['birthday']
        except:
            pass
        try:
            dict['Registry?']=dict['so']
        except:
            pass
            
    writer.writeheader()
#    writer.writerow(['ID',
#                    'Name',
#                    'Location',
#                    'Mailing Address',
#                    'Projected Parole Date',
#                    'Projected Discharge Date',
#                    'Incarcerated Date',
#                    'Birthdate',
#                    'Registry?'])
    writer.writerows(csv_dict)     
#        writer.writerow([   item['Id'],
#                            item['Alpha_Name'],
#                            item['Location'],
#                            MAILINGADDRESS
#                            item['Name']+item['Id']])
#                            item['mailing_address'][0])
#                            item['mailing_address'][1])
#                            item['mailing_address'][2]+'"',
#                            item['Parole_Date'],
#                            item['Discharge_Date'],
#                            item['Incarcerated_Date'],
#                            item['DOB'],
#                            "Yes" if item['so'] ])
    return response
