# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, reverse, HttpResponse, redirect
from models import *

from django.contrib import messages
import bcrypt
import re
from django.core.urlresolvers import reverse
from django.core import serializers
import json
from django.http import JsonResponse
from django.utils import timezone

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate 
from django.contrib.auth import logout as logout_funct
from django.contrib.auth import login as login_funct

# def home(request):
#     return redirect(reverse('resources:home'))
    
def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_funct(request,user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'registration/login.html')
    
def logout(request):
    logout_funct(request)
    return redirect(request.META.get('HTTP_REFERER'))
    
    
# def authenticate(request):
#     if request.method !='POST':
#         return redirect(reverse('main:register'))
#     username = request.POST['username']
#     password = request.POST['password']
#     check = password
#     this_user = User.objects.get(username = username)
#     this_user.save()

#     if bcrypt.checkpw(password.encode(), this_user.password.encode()):
#         request.session['current_user_id'] = this_user.id
#         return redirect(reverse('resources:home'))
#     else:
#         return redirect(reverse('main:login'))
    
# def register(request):
#      return render(request, "main/register.html")

# def create_user(request):
#     if request.method !='POST':
#         return redirect(reverse('main:register'))

#     # errors=User.objects.register_validator(request.POST)

#     # if len(errors):
#     #     for error,error_message in errors.iteritems():
#     #         messages.error(error_message)
#     #     return redirect(reverse('main:register'))

#     email = request.POST['email']
#     username = request.POST['username']
#     first_name = request.POST['first_name']
#     last_name = request.POST['last_name']
#     password = request.POST['password']
#     confirm = request.POST['confirm']
#     if password != confirm:
#         return redirect(reverse('main:register'))

#     hashed_key=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
#     User.objects.create(first_name = first_name, last_name = last_name, email = email, password=hashed_key,username=username)
#     request.session['current_first_name'] = first_name
#     request.session['current_last_name'] = last_name            
#     request.session['current_email'] = email
        
#     return redirect(reverse('main:new_user_success'))
    
# def new_user_success(request):
#     return render(request, 'main/success.html')









# Create your views here.
