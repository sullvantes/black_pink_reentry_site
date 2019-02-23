#from apps.main.models import *
from apps.update_release.models import *
from django.contrib.auth.models import User
import os

import csv
cwd = os.getcwd()
print cwd
file_name = raw_input('Enter your filename:')


cwd = os.getcwd()
print cwd
with open(file_name,'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

created_by=User.objects.get(username='test')

for x in your_list:
    this_facility = {}
    this_facility['created_by']= created_by
    this_facility['scraped_name'] = this_facility['scraped_name'] = x[0]
    this_facility['street_address']=x[1]
    this_facility['city']=x[2]
    this_facility['state']=x[3]
    this_facility['zip_code']=x[4]
    new_facility = Facility.objects.create(**this_facility)
    new_facility.save()
    print "Created Resource for " + this_facility['scraped_name']
    
#    print x
#
#admin=User.objects.get(username='kimsammons')
#for x in your_list: 
#    dedicated_to = x[1]
#    print "\t"+dedicated_to
#    name = x[2]
#    print "\t"+ name
#    county = x[3]
#    print "\t"+county
#    address = x[4]
#    print "\t"+address
#    city =x[5]
#    print "\t"+city
#    state = x[6]
#    print "\t"+state
#    zip_code = x[7]
#    print "\t"+zip_code
#    
#    phone=x[8]
#    print "\t"+phone,
#    contact_name=x[9]
#    email=x[10]
#    print "\t"+email,
#    website = x[11]
#    print "\t"+website,
#    notes=x[12]
#    print "\t"+notes,
#    restrictions=x[13]
#    print "\t"+restrictions,
#    bp_contact=x[14]
#    print "\t"+bp_contact
#    bp_supported_note=x[15]
#    print "\t"+bp_supported_note
#
#
#
#    org_bool = OrganizationType.objects.filter(name=x[0])
#    
#    if org_bool:
#        org_type = OrganizationType.objects.get(name=x[0])
#        org_type.save()
#        this_org=Organization.objects.create(dedicated_to=dedicated_to,name=name,county=county,address=address,city=city,state=state,zip_code=zip_code, phone=phone,contact_name=contact_name,email=email,website=website,notes=notes,restrictions=restrictions,bp_contact=bp_contact,bp_supported_note=bp_supported_note,created_by=admin)
#        this_org.save()
#        this_org.org_type.add(org_type)
#        print "Created Resource for " + name
#    else:
#        print "This Organiztaion Type doesn't exist...skipping..."    