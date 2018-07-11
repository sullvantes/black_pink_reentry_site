# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re 
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required

from django.db.models import Max, Q, F, Count

from models import *
from ..update_release.IL_release import *
from ..update_release.FED_release import *


# Create your views here.

@login_required
def home(request):
    all_members = Member.objects.filter(status = 'Inc').order_by('-updated_at')[:100]
    response = {
        'members' : all_members,
        }    
    return render(request, "manage_member/home.html",response)

@login_required
def add_members(request):
    if request.method=='POST':
        ids = request.POST['IDsToAdd'].replace(',','')
        list_of_ids = ids.split()
        for id in list_of_ids:
            id = re.sub('[^A-Z0-9]','', id.upper())
            if (len(id) == 6 and id[1:].isdigit()) or (len(id) == 8 and id.isdigit()) :
                if Member.objects.filter(gov_id = id).count()<1:
                    Member.objects.create(gov_id = id, created_by=request.user)
    return redirect(reverse('members:home'))

@login_required
def show(request):
    all_members = Member.objects.exclude(status='Par').order_by('last_name')
    request.session['memb_list'] = make_csv(all_members)
    response = {
        'header': "All Members Ordered by Given Last Name",
        'result':all_members, 
        'count':all_members.count(),
        }    
    return render(request, "manage_member/all_members.html", response)

@login_required
def show_by_updated(request):
    all_members = Member.objects.exclude(status='Par').order_by('updated_at')
    request.session['memb_list'] = make_csv(all_members)
    response = {
        'header': "All Members Ordered by Last Update",
        'result':all_members, 
        'count':all_members.count(),
        }    
    return render(request, "manage_member/all_members.html", response)

@login_required
def show_stale(request):
    stale_members = Member.objects.exclude(status='Par').exclude(facility__name__icontains = 'Free').filter(updated_at__lte = datetime.now()-timedelta(days=7))
    request.session['memb_list'] = make_csv(stale_members)

    response = {
        'header': "Members Needing Update",
        'result':stale_members, 
        'count':stale_members.count(),
        }    
    return render(request, "manage_member/all_members.html", response)


@login_required
def show_months(request):
    if request.method=='POST':
        request.session["months"] = request.POST['months']
    else:
        request.session["months"] = 4
    cut_off_date=datetime.now()+timedelta(days=int(request.session["months"])*30.4375)
    cut_off_date=cut_off_date.replace(day=1) 
    select_members = Member.objects.exclude(status='Par')
    select_members = select_members.filter(Q(parole_date__lt=cut_off_date) | Q(discharge_date__lt=cut_off_date))
    select_members = select_members.annotate(earliest_date = F('parole_date') if F('parole_date')!=None else F('discharge_date')).order_by('earliest_date')
    request.session['memb_list'] = make_csv(select_members) 
    cache.set('memb_list',select_members,1000)

    stale_records = Member.objects.exclude(status='Par').exclude(facility__name__icontains = 'Free').filter(updated_at__lte = datetime.now()-timedelta(days=7)).count()
    response = {
        'header': "Expected Release or Parole before %s" % cut_off_date.strftime('%b-%Y'),
        'result':select_members, 
        'stale_records' :stale_records,
        'count':select_members.count(),
        }    
    return render(request, "manage_member/all_members.html", response)

@login_required
def update_existing(request):
    response = {
        'result':request.session["idoc_result"], 
        }    
    return redirect(reverse('members:show'))

def update(request, num):
    needs_update = Member.objects.exclude(status='Par').order_by('updated_at')[:100]
    for member in needs_update:
    # try:
        #Federal IDs
        if member.gov_id.isdigit() and len(member.gov_id) == 8:
            this_dict = Fed_Member(member.gov_id).return_dict()
            try:
                this_dict['bday_abb'] = "~" + this_dict['birthday'][0:4]
            except:
                this_dict['bday_abb']=""
        # IDOC ids
        elif member.gov_id[0].isalpha() and len(member.gov_id) == 6:
            this_dict=Ill_Member(member.gov_id).return_dict()
        
        # delete bad ids
        else:
            print "This id is bad and needs to be fixed and re-added. Deleting %s" % member.gov_id
            member.delete()
            continue
        
        if 'status' in this_dict:
            if this_dict['status'] == "Par":
                if member.last_name:
                    member.facility=Facility.objects.get(name = "Free World")
                    member.status='Free World'
                    member.parole_date=None
                    member.discharge_date=None
                    print "%s was released" % member.last_name
                else:
                    member.delete()
                    print "Member was released with no info. Entry Deleted."
                    break
            else:
                # print "The facility is %s" % this_dict['facility_name']
                try:
                    member_fac = Facility.objects.get(scraped_name = this_dict['facility_name'])
                except:
                    if this_dict['typestate'] is 'FED':
                        member_fac = Facility.objects.get(scraped_name = 'Non-Illinois Federal')
                    else:
                        member_fac = Facility.objects.get(scraped_name = 'Unknown IL')            
                if member_fac is not member.facility:
                    member.facility = member_fac
                    member.save()
                    

                for key, value in this_dict.items():
                    if hasattr(member, key):
                        if key =='facility':
                            pass
                        elif getattr(member,key) != value:
                            setattr(member, key, value)
                            member_changed = True
                            # print "%s updated." % key
            member.updated_at=datetime.now()
            print "%s was updated." % member.last_name
            member.save()    
    # except:
    #     pass
    return redirect(reverse('members:show_by_updated'))

@login_required
def update_searched(request):
    username = request.user
    entry_values = ['incarcerated_date', 'parole_date','discharge_date' ]
    for entry in request.session["search_result"]:
        if entry['isValid'] == True:
        #     if Member.objects.get(gov_id=entry['gov_id']):
        #         this_member = Member.objects.get(gov_id = entry['gov_id'])
        #         for value in entry_values:
        #             try:
        #                 this_member.make_change(value, entry[value])
        #             except:
        #                 pass
        #     else:
        #         this_facility = Facility.objects.get(scraped_name=entry['facility_name'])
        #         new_member = Member(facility=this_facility,created_by=username)
        #         for key, value in entry.items():
        #             setattr(new_member, key, value)
        #         new_member.save()
        #         this_member=new_member
            entry_facility = Facility.objects.get(scraped_name = entry['facility_name'])
        # for key, value in entry.iteritems():
        #     print "\t%s : %s " % (key, value)

    response = {
        'result':request.session["search_result"], 
        }    
    return redirect(reverse('release:results'))

def update_by_id(request, id):
    member = Member.objects.get(id = id)
    # try:
    #Federal IDs
    if member.gov_id.isdigit() and len(member.gov_id) == 8:
        this_dict = Fed_Member(member.gov_id).return_dict()
        try:
            this_dict['bday_abb'] = "~" + this_dict['birthday'][0:4]
        except:
            this_dict['bday_abb']=""
    # IDOC ids
    elif member.gov_id[0].isalpha() and len(member.gov_id) == 6:
        this_dict=Ill_Member(member.gov_id).return_dict()
    
    # delete bad ids
    else:
        print "This id is bad and needs to be fixed and re-added. Deleting %s" % member.gov_id
        member.delete()
        return redirect(reverse('members:show_months'))
    
    if 'status' in this_dict:
        if this_dict['status'] == "Par":
            if member.last_name:
                member.facility=Facility.objects.get(name = "Free World")
                member.status='Free World'
                member.parole_date=None
                member.discharge_date=None
                print "%s was released" % member.last_name
                member.save()
            else:
                member.delete()
                print "Member was released with no info. Entry Deleted"
            return redirect(reverse('members:show_months'))
        else:
            # print "The facility is %s" % this_dict['facility_name']
            try:
                member_fac = Facility.objects.get(scraped_name = this_dict['facility_name'])
            except:
                if this_dict['typestate'] is 'FED':
                    member_fac = Facility.objects.get(scraped_name = 'Non-Illinois Federal')
                else:
                    member_fac = Facility.objects.get(scraped_name = 'Unknown IL')            
            if member_fac is not member.facility:
                member.facility = member_fac
                member.save()
                

            for key, value in this_dict.items():
                if hasattr(member, key):
                    if key =='facility':
                        pass
                    elif getattr(member,key) != value:
                        setattr(member, key, value)
                        member_changed = True
                        # print "%s updated." % key
        member.updated_at=datetime.now()
        print "%s was updated." % member.last_name
        member.save()    
# except:
    #     pass
    return redirect(reverse('members:show_months'))


def csv_print(request):
    # Create the HttpResponse object with the appropriate CSV header.
    
    csv_dict = request.session['memb_list']
    timestr = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename="Release_Upcoming_"+timestr+".csv"
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
                    'Note'
                 ]

    writer = csv.DictWriter(response, dialect='excel', fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(csv_dict)     
    return response

def make_csv(queryset):
    csv_rows=[]
    for member in queryset:
        note = ''
        this_row = {}
        try:
            if member.msr:
                note += 'MSR '
        except:
            pass

        try:
            if member.so:
                note += 'On Reg '
        except:
            pass

        try:
            if member.life:
                note += 'Life '
        except:
            pass
    
        address ="%s %s %s" % (member.first_name, member.last_name, member.gov_id)
        address+= "\n%s" %  member.facility.name
        address+= "\n%s" %  member.facility.street_address
        address+= "\n%s, %s %s" %  (member.facility.city,member.facility.state,member.facility.zip_code)
        this_row['ID'] = member.gov_id 
        this_row['Name'] = member.last_name +", "+member.first_name
        this_row['Location'] = member.facility.name
        this_row['Address'] = address
        this_row['Projected Parole Date'] = date_str(member.parole_date)
        this_row['Projected Discharge Date'] = date_str(member.discharge_date)
        this_row['Incarcerated Date'] = date_str(member.incarcerated_date)
        this_row['Birthday'] = date_str(member.birth_date)
        this_row['Note'] = note
        
        csv_rows.append(this_row)
    return csv_rows

def date_str(date):
    if date:
        return "%s/%s/%s" % (date.year, date.month, date.day)

