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
    logged_in = False
    user=''
    admin = False
    if 'current_user_id' in request.session :
        print request.session['current_user_id']
        logged_in = True
        current_id = request.session['current_user_id']
        current_user = User.objects.get(id=current_id)
        user=current_user.username
        if current_user.username=='admin':
            admin = True
    cities = Resource.objects.values('city','state').distinct()
    response = {
        'username': user,
        'admin': admin,
        'logged_in':logged_in, 
        'cities':cities,
        }    
    return render(request, "resources/home.html",response)

def all_orgs(request):
    logged_in = False
    user=''
    admin = False
    if 'current_user_id' in request.session :
        print request.session['current_user_id']
        logged_in = True
        current_id = request.session['current_user_id']
        current_user = User.objects.get(id=current_id)
        user=current_user.username
        if current_user.username=='admin':
            admin = True
    all_resources = Resource.objects.all()
    title = "All Resources"
    response = {
        'username': user,
        'admin': admin,
        'logged_in':logged_in, 
        'all_resources':all_resources,
        'title': title,   
        }    
    return render(request, "resources/all.html",response)

def modal(request):
    logged_in = False
    user=''
    admin = False
    if 'current_user_id' in request.session :
        print request.session['current_user_id']
        logged_in = True
        current_id = request.session['current_user_id']
        current_user = User.objects.get(id=current_id)
        user=current_user.username
        if current_user.username=='admin':
            admin = True
    first_resource = Resource.objects.all()[0]
    title = "First Resource"
    response = {
        'username': user,
        'admin': admin,
        'logged_in':logged_in, 
        'first_resource':first_resource,
        'title': title,   
        }    
    return render(request, "resources/modal.html",response)

def org_home(request,org_id):
    logged_in = False
    user=''
    admin = False
    if 'current_user_id' in request.session :
        print request.session['current_user_id']
        logged_in = True
        current_id = request.session['current_user_id']
        current_user = User.objects.get(id=current_id)
        user=current_user.username
        if current_user.username=='admin':
            admin = True
    this_org = Resource.objects.get(id=org_id)
    form = ResourceForm(None, instance=this_org)
    title = this_org.name + " Home"
    response = {
        'username': user,
        'admin': admin,
        'logged_in':logged_in, 
        'org': this_org,
        'title': title,   
        'form' : form,
        }    
    return render(request, "resources/org_home.html",response)

@login_required
def add_org(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ResourceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return redirect(reverse ('resources:all_orgs'))

    # if a GET (or any other method) we'll create a blank form
    else:
            title = "Add New Resource"
            form = ResourceForm()
            response = {
            'form': form,
            }
            return render(request, 'resources/add_org.html', response)

def test(request):
    return render(request, 'resources/test.html')


# Create your views here.
