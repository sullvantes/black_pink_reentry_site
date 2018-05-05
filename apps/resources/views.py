# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import models 
from models import *
from forms import *


def home(request):
    all_resource_types = ResourceType.objects.all()        
    cities = Resource.objects.values('city','state').distinct()
    all_resources = Resource.objects.all()
    response = {
        'cities':cities,
        'resources' : all_resources,
        'all_resource_types' : all_resource_types,
        'resourcetype' : "All"
        }    
    return render(request, "resources/home.html",response)

def search_types(request):
    if request.method == 'POST' and request.POST['resource_type'] != "":
        print request.POST['resource_type']
        return redirect(reverse('resources:resource_type', kwargs = {'resource_type_id' : request.POST['resource_type']}))
    return redirect(reverse('resources:home'))

def resource_type(request, resource_type_id):
    all_resource_types = ResourceType.objects.all()        
    resource_type = ResourceType.objects.get(id = resource_type_id)
    resources = Resource.objects.filter(resource_types = resource_type)
    cities = Resource.objects.values('city','state').distinct()
    response = {
        'cities': cities, 
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
    print request.user
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
    return render(request, "resources/edit.html",response)


@login_required
def add_resource(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print "its a POST"
        print request.POST
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
    


# Create your views here.
