from apps.main.models import *
from apps.resources.models import *
import bcrypt

admin=User.objects.filter(username='admin')
if not admin:
    print "creating admin User..."
    hashed_key=bcrypt.hashpw('n0m0repris0ns'.encode('utf-8'), bcrypt.gensalt())

    User.objects.create(first_name="admin",last_name="admin",
    username="admin",
    email="sullyut@gmail.com",password=hashed_key)
    
else:
    print "admin user already present...\n"
admin=User.objects.get(username='admin')
print "Creating Org Types"
org_types =[['Necessaries','These are things that everyone needs'],
['Housing','Resources for Housing'],['Employment','Resources for finding employment'],
['Legal','Legal Resources'],
['LGBT Health','These are resources specifically for LGBT Health'],
['Mental Health','Mental Health Resources'],['Recovery','Resources for Recovery From Addiction']]


for type in org_types:
    curr_type = OrganizationType.objects.filter(name = type[0])
    if curr_type:
        print "\t"+type[0] + " is already present..."
    else:
        OrganizationType.objects.create(name=type[0],description=type[1],created_by=admin)
        print "\tCreated Organization Type called " + type[0]


     