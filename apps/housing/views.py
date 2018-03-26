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
        'nearby_locations':request.session['nearby_locations'],
        'valid_address':request.session['valid_address']
        }    
    return render(request, "housing/results.html", response)