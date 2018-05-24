# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fpdf import FPDF, HTMLMixin
import os
import datetime
import csv
# from PIL import Image

from django.http import HttpResponse

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import models 
from django.db.models import Min
from django.conf import settings

from models import *
from forms import *


#shows all resources
def home(request):
    # clear current resources types from session cache
    if 'curr_resource_types' in request.session:
        request.session['curr_resource_types']=None
    all_resource_types = ResourceType.objects.all()        
    all_resources = Resource.objects.filter(approved = True).annotate(main_type = Min('resource_types__name'))
    response = {
        'resources' : all_resources,
        'all_resource_types' : all_resource_types,
        'resourcetype' : "All"
        }    
    return render(request, "resources/home.html",response)

# creates session cache from post request
def search_types(request):
    if request.method == 'POST':
        if 'type' in request.POST:
            if request.POST['type'] =='*':
                return redirect(reverse('resources:home'))
            types = [request.POST['type']]
        else:
            types = []
            for k,v in request.POST.items():
                if 'type' in k:
                        types.append(k.strip('types_'))
        request.session['curr_resource_types']=types
        return redirect(reverse('resources:resource_list'))
    return redirect(reverse('resources:home'))

# For Linking to resource types    
def resource_type(request, resource_type_id):
    types = [resource_type_id]
    request.session['curr_resource_types']=types
    return redirect(reverse('resources:resource_list'))

#creates resource list from session cache
def resource_list(request):
    if 'curr_resource_types' in request.session:
        all_resource_types = ResourceType.objects.all()
        resource_types = request.session['curr_resource_types']
        resource_list = Resource.objects.filter(approved = True, resource_types__in= resource_types )
        resources = resource_list.annotate(main_type = Min('resource_types__name'))
    else:
        return redirect(reverse('resources:home')) 

    if len(resource_types) == 1:
        resource_type = ResourceType.objects.get(id__in = resource_types)
    else:
        resource_type = 'Selected'
    response = {
        'resources' : resources,
        'all_resource_types' : all_resource_types,
        'resourcetype' : resource_type,
        }    
    return render(request, "resources/home.html", response)


def view_resource(request,resource_id):
    if request.user.is_authenticated:
        return redirect(reverse('resources:edit_resource', kwargs = {'resource_id' : resource_id}))
    this_resource = Resource.objects.get(id=resource_id)
    
    try:
        resource_type = ResourceType.objects.filter(resources__id=resource_id)[0]
        try:
            other_resources = Resource.objects.exclude(id=resource_id).filter(resource_types__name = resource_type)[:10]
        except:
            other_resources = Resource.objects.filter(approved = True, resource_types__name = resource_type) 
    except:
        other_resources = Resource.objects.filter(approved = True)[:10]

    all_resource_types = ResourceType.objects.all()
    response = {
        'resource': this_resource,
        'other_resources': other_resources,
        'resource_types' : all_resource_types,
        }    
    return render(request, "resources/view.html",response)

def edit_resource(request,resource_id):
    this_resource = Resource.objects.get(id=resource_id)
    if this_resource.created_by == None:
        this_resource.created_by = request.user
    form = ResourceForm(instance=this_resource)
    
    try:
        resource_type = ResourceType.objects.filter(resources__id=resource_id)[0]
        try:
            other_resources = Resource.objects.exclude(id=resource_id).filter(resource_types__name = resource_type)[:10]
        except:
            other_resources = Resource.objects.filter(approved = True, resource_types__name = resource_type) 
    except:
        other_resources = Resource.objects.filter(approved = True)[:10]
    
    all_resource_types = ResourceType.objects.all()

    response = {
        'resource': this_resource,
        'form' : form,
        'other_resources': other_resources,
        'resource_types' : all_resource_types,
        }    
    return render(request, "resources/edit.html", response)

def submit_resource(request):
    if request.user.is_authenticated:
        return redirect(reverse ('resources:add_resource'))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        new_resource_data=request.POST.copy()
        new_resource_data['created_by']=request.user
        new_resource_data['approved']=False
        new_resource_data['approved_by']=None

        form = ResourceForm(request.POST)
      
        if form.is_valid:   
            new_resource = form.save(commit=False)
            new_resource.created_by = request.user
            new_resource.save()
            return redirect(reverse('resources:thanks'))
    else:
        form = ResourceForm()
    other_resources = Resource.objects.filter(approved = True)[:10]

    all_resource_types = ResourceType.objects.all()
    response = {
        'form' : form,
        'other_resources': other_resources,
        'resource_types' : all_resource_types,
        }    
    return render(request, "resources/submit.html",response)

def add_resource(request):
    if not request.user.is_authenticated:
        return redirect(reverse ('resources:submit_resource'))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        new_resource_data=request.POST.copy()
        new_resource_data['created_by']=request.user
        new_resource_data=request.POST.copy()
        new_resource_data['created_by']=request.user
        new_resource_data['approved']=request.user
        new_resource_data['approved_by']=None
        form = ResourceForm(request.POST)
      
        if form.is_valid:
            print form.errors    
            new_resource = form.save(commit=False)
            new_resource.created_by = request.user
            new_resource.save()
        print form.errors

        return redirect(reverse ('resources:view_resource', kwargs = { 'resource_id': new_resource.id}))

    else:
        form = ResourceForm()
        other_resources = Resource.objects.filter(approved = True)[:10]
    
        all_resource_types = ResourceType.objects.all()
        response = {
            'form' : form,
            'other_resources': other_resources,
            'resource_types' : all_resource_types,
            }    
        return render(request, "resources/add.html",response)

def save_resource(request, resource_id):
    # if this is a POST request we need to process the form data
    print "routed correctly"
    if request.method == 'POST':
        print "its a POST"
        print request.POST
        this_resource =Resource.objects.get(id = resource_id)
        # create a form instance and populate it with data from the request:
        # new_org_dict = request.POST
        # new_org_dict['created_by'] = request.user
        form = ResourceForm(instance = this_resource, data = request.POST)

        # check whether it's valid:
        if form.is_valid():
            print "its valid"
            resource = form.save()
        print form.errors
            
        return redirect(reverse ('resources:view_resource', kwargs = { 'resource_id': resource.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        return redirect(reverse('resources: home'))

def confirm_delete(request, resource_id ):
    this_resource = Resource.objects.get(id=resource_id)

    try:
        resource_type = ResourceType.objects.filter(resources__id=resource_id)[0]
        try:
            other_resources = Resource.objects.exclude(id=resource_id).filter(resource_types__name = resource_type)[:10]
        except:
            other_resources = Resource.objects.filter(approved = True, resource_types__name = resource_type) 
    except:
        other_resources = Resource.objects.filter(approved = True)[:10]

    all_resource_types = ResourceType.objects.all()
    response = {
        'resource': this_resource,
        'other_resources': other_resources,
        'resource_types' : all_resource_types,
        }    
    return render(request, 'resources/confirm_delete.html', response)

def delete_resource(request):
    if request.method == 'POST':
        this_resource = Resource.objects.get(id=request.POST['resource_id'])
        this_resource.delete()
    return redirect(reverse('resources:home'))


def if_none(attr):
    if attr ==None:
        return ''
    else:
        return attr

class MyFPDF(FPDF, HTMLMixin):
    def header(self):
        # Logo
        # self.image('media/download.jpeg', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(50)
        # Title
        self.cell(93, 10, 'Black And Pink Re-Entry Resources')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-20)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')
        self.set_y(-15)
        self.cell(0, 10, "Created: "+datetime.datetime.now().strftime("%b %d %Y %H:%M:%S"), 0, 0, 'C')     
    pass

def pdf_print_resources(request):
    if 'curr_resource_types' in request.session and request.session['curr_resource_types'] != None:
        resource_types = request.session['curr_resource_types']
        resource_list = Resource.objects.filter(approved = True, resource_types__in= resource_types)
        resource_types = ResourceType.objects.filter(id__in= resource_types )
    else:
        resource_types = ResourceType.objects.all()
        resource_list = Resource.objects.filter(approved = True)
    resources = resource_list.annotate(main_type = Min('resource_types__name'))
    html = ""
    for resource_type in resource_types:
        html += "<h1 style='page-break-before: always'>%s</h1>" % resource_type
        these_resources = resources.filter(main_type = resource_type)
        for resource in these_resources:
            html += "<h3>%s</h3>" % resource.name
            if resource.phone:
                html += "<B>Phone:</B> <a href='tel:%s'>%s</a> " % (resource.phone,resource.phone) 
            if resource.email:
                html += "<B>Email:</B> <a href='mailto:%s'>%s</a>" % (resource.email,resource.email)
            if resource.website:
                html += "<B>Website:</B> <a href='%s'>%s</a><br>" % (resource.website,resource.website)
            if resource.address:
                html += "<B>Address:</B> %s &nbsp;&nbsp;&nbsp;&nbsp;" % resource.address
            if resource.city:
                html += "&nbsp;&nbsp;&nbsp;&nbsp;%s, " % resource.city
                if resource.state:    
                    html += " %s " % resource.state
                else:
                    html += " IL "
                if resource.zip_code:
                  html += "&nbsp;%s" % resource.zip_code
            
            html+="<br>"
            if resource.contact_name:
                html += "<B>Organization Contact:</B> %s<br>" % resource.contact_name
            if resource.notes:
                html += "<B>Notes:</B><br>%s<br>" % resource.notes
            if resource.restrictions:
                html += "<B>Restrictions:</B><br>%s<br>" % resource.restrictions
            if resource.bp_contact:
                html += "<B>Black And Pink Contact:</B> %s<br>" % resource.bp_contact
            if resource.bp_supported_note:
                html += "<B>Black And Pink Note:<B/> %s<br>" % resource.bp_supported_note  

    html=html.replace(u"\u2018", "'").replace(u"\u2019", "'")

    file_path = os.path.join(settings.MEDIA_ROOT, "resource_list.pdf")
    pdf=MyFPDF()
    pdf.add_page()
    pdf.write_html(html)
    pdf.output(file_path,'F')
    if os.path.exists('resource_list.pdf'):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename=resource_list.pdf'
        os.remove(file_path)    
        return response
    return redirect(reverse('resources:resource_list'))
    
def csv_print_resources(request):
    # Create the HttpResponse object with the appropriate CSV header.

    timestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename="Resource_List"+timestr+".csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+filename
    
    writer = csv.writer(response,dialect='excel')

    fieldnames = [  'Resource Type', 
                    'Org Name', 
                    'Address',
                    'Phone',
                    'Org Contact',
                    'Email',
                    'Website',
                    'Description',
                    'Restrictions/Considerations'
                    'BP Contact',
                    'BP Supported Note'
                 ]

    if 'curr_resource_types' in request.session and request.session['curr_resource_types'] != None:
        resource_types = request.session['curr_resource_types']
        resource_list = Resource.objects.filter(approved = True, resource_types__in= resource_types)
        resource_types = ResourceType.objects.filter(id__in= resource_types )
    else:
        resource_types = ResourceType.objects.all()
        resource_list = Resource.objects.filter(approved = True)
    resources = resource_list.annotate(main_type = Min('resource_types__name'))
    csv_dict=[]
    for resource in resources:
        this_dict = {}    
        this_dict['Resource Type'] = (resource.main_type if resource.main_type else "")
        this_dict['Org Name'] = (resource.name if resource.name else "")
        this_dict['Address'] = "%s %s %s %s" % (resource.address,resource.city,resource.state,resource.zip_code)
        this_dict['Phone'] = (resource.phone if resource.phone  else "")
        this_dict['Org Contact'] = (resource.contact_name if resource.contact_name else "")
        this_dict['Description'] = (resource.notes if resource.notes else "")
        this_dict['Restrictions/Considerations'] = (resource.restrictions if resource.restrictions else "")
        this_dict['BP Contact'] = (resource.bp_contact if resource.bp_contact else "")
        this_dict['BP Supported Note'] = (resource.bp_supported_note if resource.bp_supported_note else "")
        for key, value in this_dict.items():
            this_dict[key]=this_dict[key].replace(u"\u2018", "'").replace(u"\u2019", "'")
        csv_dict.append(this_dict)

    writer = csv.DictWriter(response, dialect='excel', fieldnames=fieldnames, extrasaction='ignore')      
    writer.writeheader()
    writer.writerows(csv_dict)     
    return response

