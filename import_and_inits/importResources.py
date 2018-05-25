from django.db import models
from apps.main.models import *
from apps.resources.models import *
import csv


with open("EXP_REENTRY.csv",'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)
all_resource_types = ResourceType.objects.all()
for resource_type in all_resource_types:
    print resource_type
input_resource = raw_input("Type of Resource to Import===>")
resource_type = ResourceType.objects.get(name=input_resource)
if resource_type:
    print "Got Resource Type %s" % resource_type
    delete = None 
    while delete not in ['y','N']: 
        delete= raw_input("Replace all resources...Delete other '%s' resources? y or N.....") 
    if delete == 'y':
        Resource.objects.filter(resource_types=resource_type).delete()

    admin=User.objects.get(username='bpadmin')
    # count =0
    # for x in your_list[0]: 
    #     print count, x
    #     count+=1
    print "test"
    for resource in your_list[1:]:
        # print resource
        if resource[1]:    
            new_resource=Resource(created_by=admin, name=resource[1],approved=True)
            new_resource.save()
            # new_resource.created_by=admin
            # new_resource.name=resource[1]
            print "Created Resource for %s" % resource[1] 
            if resource[2]:
                new_resource.city=resource[2]
                new_resource.state='IL'
                print "\tAdded City State"
            if resource[3]:
                new_resource.address=resource[3]
                print "\tAdded Address"
            if resource[4]:
                new_resource.phone=resource[4]
                print "\tAdded Phone"
            if resource[5]:
                new_resource.contact_name=resource[5]
                print "\tAdded Contact Name"
            if resource[6]:
                new_resource.email=resource[6]
                print "\tAdded Email"
            if resource[7]:
                new_resource.website=resource[7]
                print "\tAdded Website"
            if resource[0]:
                notes=resource[0]
                if resource[8]:
                    notes+=resource[8]
                new_resource.notes=notes
                print "\tAdded notes"
            elif resource[8]:        
                new_resource.notes=resource[8]
                print "\tAdded notes"
            restrictions = resource[9]
            if resource[10]:
                restrictions+=" LGBTQ friendly? %s" % resource[10]
            if resource[12]:
                restrictions+=" Sex Offenses Ok?: %s" % resource[12]
            if restrictions:
                new_resource.restrictions=restrictions 
                print "\tAdded notes"
            new_resource.save()
            new_resource.resource_types.add(resource_type)
    # dedicated_to = x[1]
    # print "\t"+dedicated_to
    # name = x[2]
    # print "\t"+ name
    # county = x[3]
    # print "\t"+county
    # address = x[4]
    # print "\t"+address
    # city =x[5]
    # print "\t"+city
    # state = x[6]
    # print "\t"+state
    # zip_code = x[7]
    # print "\t"+zip_code
    
    # phone=x[8]
    # print "\t"+phone,
    # contact_name=x[9]
    # email=x[10]
    # print "\t"+email,
    # website = x[11]
    # print "\t"+website,
    # notes=x[12]
    # print "\t"+notes,
    # restrictions=x[13]
    # print "\t"+restrictions,
    # bp_contact=x[14]
    # print "\t"+bp_contact
    # bp_supported_note=x[15]
    # print "\t"+bp_supported_note



    # org_bool = OrganizationType.objects.filter(name=x[0])
    
    # if org_bool:
    #     org_type = OrganizationType.objects.get(name=x[0])
    #     org_type.save()
    #     this_org=Organization.objects.create(dedicated_to=dedicated_to,name=name,county=county,address=address,city=city,state=state,zip_code=zip_code, phone=phone,contact_name=contact_name,email=email,website=website,notes=notes,restrictions=restrictions,bp_contact=bp_contact,bp_supported_note=bp_supported_note,created_by=admin)
    #     this_org.save()
    #     this_org.org_type.add(org_type)
    #     print "Created Resource for " + name
    # else:
    #     print "This Organiztaion Type doesn't exist...skipping..."    