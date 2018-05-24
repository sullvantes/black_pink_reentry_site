# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from fpdf import FPDF, HTMLMixin
import os
import datetime
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

#shows all resources
def home(request):
    # clear current resources types from session cache
    if 'curr_resource_types' in request.session:
        request.session['curr_resource_types']=None
    all_resource_types = ResourceType.objects.all()        
    all_resources = Resource.objects.all().annotate(main_type = Min('resource_types__name'))
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
        resource_list = Resource.objects.filter(resource_types__in= resource_types )
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
            other_resources = Resource.objects.filter(resource_types__name = resource_type) 
    except:
        other_resources = Resource.objects.all()[:10]

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
            other_resources = Resource.objects.filter(resource_types__name = resource_type) 
    except:
        other_resources = Resource.objects.all()[:10]
    
    all_resource_types = ResourceType.objects.all()

    response = {
        'resource': this_resource,
        'form' : form,
        'other_resources': other_resources,
        'resource_types' : all_resource_types,
        }    
    return render(request, "resources/edit.html", response)


@login_required
def add_resource(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        new_resource_data=request.POST.copy()
        new_resource_data['created_by']=request.user
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
        other_resources = Resource.objects.all()[:10]
    
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
            other_resources = Resource.objects.filter(resource_types__name = resource_type) 
    except:
        other_resources = Resource.objects.all()[:10]

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

def make_list(request):
    all_resource_types = ResourceType.objects.all()        
    response = {
                'all_resource_types' : all_resource_types,
    }
    return render(request, 'resources/make_list.html', response)


# <H1 align="center">Black And Pink Re-Entry Resourses</H1>
# <p>You can now easily print text while mixing different
# styles : <B>bold</B>, <I>italic</I>, <U>underlined</U>, or
# <B><I><U>all at once</U></I></B>!
 
# <BR>You can also insert hyperlinks
# like this <A HREF="http://www.mousevspython.com">www.mousevspython.comg</A>,
# or include a hyperlink in an image. Just click on the one below.<br>
# <center>
# <A HREF="http://www.mousevspython.com"></A>
# </center>
 
# <h3>Sample List</h3>
# <ul><li>option 1</li>
# <ol><li>option 2</li></ol>
# <li>option 3</li></ul>


# def make_table_data(qset):
#     html = """

# <table border="0" align="center" width="100%">
# <thead><tr>
#     <th width="5%">Org</th>
#     <th width="5%">City</th>
#     <th width="10%">Address</th>
#     <th width="10%">Phone</th>
#     <th width="10%">Org Contact</th>
#     <th width="5%">Email</th>
#     <th width="10%">Website</th>
#     <th width="20%">Description</th>
#     <th width="15%">Restrictions/Considerations</th>
#     <th width="10%">BP Contact</th>
#     <th width="5%">Supported?</th>
#     <th width="5%">Added</th>
# </tr></thead>
# <tbody>
# """
#     for resource in qset:
#         try:
#             html+="""
# <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
# """ % (if_none(resource.name), if_none(resource.city), if_none(resource.address), if_none(resource.phone), if_none(resource.contact_name), if_none(resource.email), if_none(resource.website), if_none(resource.notes), if_none(resource.restrictions), if_none(resource.bp_contact), if_none(resource.bp_supported_note), if_none(resource.created_at))
#         except:
#             pass
#     html+= """
    
# </tbody>
# </table>
# """
#     html=html.replace(u"\u2018", "'").replace(u"\u2019", "'")
#     return html




#   for resource in qset:
#         html += """
# <h3>%s</h3>
# <ul><li>%s</li>
# <ol><li>%s</li></ol>
# <li>%s</li></ul>
# """% (if_none(resource.name), if_none(resource.city), if_none(resource.address), if_none(resource.phone))
#     html=html.replace(u"\u2018", "'").replace(u"\u2019", "'")
#     return html
def pdf_print_resources(request):
    if 'curr_resource_types' in request.session and request.session['curr_resource_types'] != None:
        resource_types = request.session['curr_resource_types']
        resource_list = Resource.objects.filter(resource_types__in= resource_types)
        resource_types = ResourceType.objects.filter(id__in= resource_types )
    else:
        resource_types = ResourceType.objects.all()
        resource_list = Resource.objects.all()
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

    timestr = time.strftime("%Y%m%d_%H%M%S")
    filename="Resource_List"+timestr+".csv"
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

