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
        needs_update = Member.objects.exclude(status='Par').order_by('-updated_at')[:10]
        
        for member in needs_update:
            try:
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
                    try:
                        this_dict['bday_abb'] = this_dict['birthday'][0:4]+'/'+this_dict['birthday'][4:2]+'/'+this_dict['birthday'][6:2]
                    except:
                        this_dict['bday_abb']=""    
                # delete bad ids
                else:
                    print "This id is bad and needs to be fixed and re-added. Deleting %s" % member.gov_id
                    member.delete()
                    pass

                print this_dict['given_name_alpha']
                member_changed = False
                if 'status' in this_dict:
                    if this_dict['status'] !=   "Par":
                        # print this_dict['facility_name']   
                        member_fac = Facility.objects.get(scraped_name = this_dict['facility_name'])
                        if member_fac is not member.facility:
                            member.facility = member_fac
                            member.save()
                            # print "new facility added"
                            member_changed = True
                
                        # except:
                        #     print "need to add %s to facilities" % this_dict['facility_name']

                        for key, value in this_dict.items():
                            if hasattr(member, key):
                                if key =='facility':
                                    # if member['facility'] == None:
                                    #     member.facility = member_fac
                                    #     member_changed = True
                                    # elif member_fac is not member['facility']:
                                    #     member.facility = member_fac  
                                    #     member_changed = True
                                    pass
                                elif 'date' in key:
                                    db_date_str = getattr(member,key).strftime("%Y-%m-%d")
                                    if db_date_str != value:
                                        setattr(member, key ,value)
                                        # print "%s updated." % key
                                elif getattr(member,key) != value:
                                    setattr(member, key, value)
                                    member_changed = True
                                    print "%s updated." % key
                    else:
                        member.facility=Facility.objects.get(name = "Free World")
                        member.status='Par'
                        print "member has been released"
                        
                    member.updated_at=datetime.now(pytz.utc)
                    if member_changed:
                        member.updated_at=datetime.now(pytz.utc)
                        print "%s was updated." % member.given_name
                    member.save()    
            except:
                pass