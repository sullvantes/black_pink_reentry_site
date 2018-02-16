import urllib2
import json
import re
from datetime import datetime, date

from models import Facility
from ..manage_member.models import *


class Fed_Member(object):
    def __init__(self,id):
        self.id = id
        self.url = 'https://www.bop.gov/PublicInfo/execute/inmateloc?todo=query&output=json&inmateNumType=IRN&inmateNum='
        self.is_valid_id()
        req = urllib2.Request(self.url + self.id)
        response = urllib2.urlopen(req)
        json_stats = json.load(response)
        if len(json_stats['InmateLocator']) >= 1:
            self.json_inmate = json_stats['InmateLocator'][0]
        else:
            self.json_inmate = None
        print "Building",self.id,"..."
    
    def return_dict(self):
        member_dict = {}
        member_dict['gov_id'] = self.id
        member_dict['typestate']='FED'
        member_dict['isValid'] = self.isValid()
        if not self.isValid():
            member_dict['given_name_alpha']= "is not a valid Federal ID"
            member_dict['facility_name']=None 
            return member_dict    
        member_dict['given_name']= self.get_name()
        member_dict['given_name_alpha']= self.get_alpha_name()
        member_dict['discharge_date']=self.get_discharge_date()
        member_dict['facility_name']=self.json_inmate['faclName']
        member_age = self.json_inmate['age']
        member_dict['birthday']= str(datetime.now().year-int(member_age))+'0000'
        
        return member_dict
    
    def make_new_member(self):
        new_member = Member(self.return_dict())
        new_member.save()
            
            
            
    def is_valid_id(self):
        if (len(self.id)!=8) or not self.id.isdigit(): 
            return False
        return True
    
    def get_alpha_name(self):
        name=self.json_inmate['nameLast']+", "+self.json_inmate['nameFirst']+" "+self.json_inmate['nameMiddle']
        return name.title()
    
    def get_name(self):
        name=self.json_inmate['nameFirst']+" "+self.json_inmate['nameMiddle']+" "+self.json_inmate['nameLast']
        return name.title()
    
    def isValid(self):
        if self.json_inmate is None:
            return False
        return True
        
    def get_discharge_date(self):
        try:
            discharge_date_obj = datetime.strptime(self.json_inmate['projRelDate'],'%m/%d/%Y')
            return discharge_date_obj.strftime('%Y-%m-%d')
        except:
            return "No Date Given"
        

# test=Fed_Member('34475018').return_dict()
# for key, value in test.iteritems():
#     print key+" : "+value