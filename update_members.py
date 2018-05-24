from datetime import datetime, timedelta

from django.db import models

from apps.update_release.models import *
from apps.manage_member.models import *

from apps.update_release.IL_release import *
from apps.update_release.FED_release import *


needs_update = Member.objects.filter(updated_at__gte=datetime.now()-timedelta(days=7))
for member in needs_update:
    if member.gov_id.isdigit():
        this_dict = Fed_Member(member.gov_id).return_dict()
        try:
            this_dict['bday_abb'] = "~" + this_dict['birthday'][0:4]
        except:
            this_dict['bday_abb']=""
    else:
        this_dict=Ill_Member(member.gov_id).return_dict()
        try:
            this_dict['bday_abb'] = this_dict['birthday'][0:4]+'/'+this_dict['birthday'][4:2]+'/'+this_dict['birthday'][6:2]
        except:
            this_dict['bday_abb']=""    
    try:
        memb_fac = Facility.objects.get(scraped_name = memb['facility_name'])
        this_dict['mailing_address']=memb_fac.mailing_address()
    except:
        this_dict['mailing_address']=[[],[],[]]

    for key, value in this_dict.items():
        try:
            member[key]=value
        except:
            pass
    member.save()