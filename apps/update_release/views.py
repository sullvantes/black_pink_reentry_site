# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from models import *
import sys
import string
from IL_release import *
from FED_release import *


def home(request):
    logged_in = False
    user=''
    admin = False
    if 'current_user_id' in request.session :
        logged_in = True
        current_id = request.session['current_user_id']
        current_user = User.objects.get(id=current_id)
        user=current_user.username
        if current_user.username=='admin':
            admin = True
    response = {
        'username': user,
        'admin': admin,
        'logged_in':logged_in, 
        }    
    return render(request, "update_release/home.html",response)

def ind_search(request):
    if request.method !="POST":
        return redirect(reverse('release:home')) 
    id_string=request.POST['govID'].replace(',','')
    allIds = id_string.split()
    request.session['search_member'] =[]
    print allIds
    request.session['search_members'] = allIds
    return redirect(reverse('release:results'))

def results(request):
    logged_in = False
    user=''
    admin = False
    if 'current_user_id' in request.session :
        logged_in = True
        current_id = request.session['current_user_id']
        current_user = User.objects.get(id=current_id)
        user=current_user.username
        if current_user.username=='admin':
            admin = True
    print request.session['search_members']    
    
    idoc_result=[]    
    for raw_id in request.session['search_members']:
        id = re.sub('[^A-Z0-9]','', raw_id.upper())
        if len(id) == 8 and id.isdigit():
            
            idoc_result.append(Fed_Member(id).return_dict())

        else:
            idoc_result.append(Ill_Member(id).return_dict())

    request.session["idoc_result"]=idoc_result
    response = {
        'username': user,
        'admin': admin,
        'logged_in':logged_in,
        'result':idoc_result, 
        }    
    return render(request, "update_release/results.html", response)

def results_hidden(request):
    logged_in = False
    user=''
    admin = False
    if 'current_user_id' in request.session :
        logged_in = True
        current_id = request.session['current_user_id']
        current_user = User.objects.get(id=current_id)
        user=current_user.username
        if current_user.username=='admin':
            admin = True
    
    idoc_result=[]    
    for id in request.session['search_members']:
         idoc_result.append(Ill_Member(id).return_dict())
    request.session["idoc_result"]=idoc_result
    response = {
        'username': user,
        'admin': admin,
        'logged_in':logged_in,
        'result':request.session["idoc_result"], 
        }    
    return render(request, "update_release/results_hidden.html", response)
    