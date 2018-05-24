from datetime import datetime, timedelta
import pytz

from django.db import models
from django.core.management.base import BaseCommand, CommandError

from apps.update_release.models import *
from apps.manage_member.models import *

from apps.update_release.IL_release import *
from apps.update_release.FED_release import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        needs_update = Member.objects.all()
        # member = Member.objects.get(gov_id = 'Y22449')
        for member in needs_update:
            try:
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


                # member.update(**this_dict)
                for key, value in this_dict.items():
                    try:
                        setattr(member, key, value)
                        # print "%s updated." % key 
                    except:
                        pass
                member.checked_at=datetime.now(pytz.utc)
                member.updated_at=datetime.now(pytz.utc)
                member.save()
            except:
                pass