
import requests
from datetime import datetime, timedelta

# from models import Facility
# from ..manage_member.models import *

fed_url = 'https://www.bop.gov/PublicInfo/execute/inmateloc?todo=query&output=json&inmateNumType=IRN&inmateNum='

class Fed_Member(object):
    def __init__(self,id):
        self.id = id
        self.is_valid_id()
        req = requests.get(fed_url + self.id)
        # response = urllib3.urlopen(req)
        json_stats = req.json()
        if len(json_stats['InmateLocator']) >= 1:
            self.json_inmate = json_stats['InmateLocator'][0]
        else:
            self.json_inmate = None
        # print "Building",self.id,"..."
    
    def return_dict(self):
        member_dict = {}
        member_dict['gov_id'] = self.id
        member_dict['typestate']='FED'
        member_dict['isValid'] = self.isValid()
        if not self.isValid():
            member_dict['last_name']= "is not a valid Federal ID"
            member_dict['facility_name']=None 
            return member_dict    
        member_dict['first_name']= self.get_first_name()
        member_dict['last_name']= self.get_last_name()
        member_dict['discharge_date']=self.get_discharge_date()
        member_dict['facility_name']=self.json_inmate['faclName']
        member_age = self.json_inmate['age']
        year = timedelta(days=365)
        age=int(member_age)*year
        approx_birthday=datetime.now().replace(day=1,month=1)-age
        member_dict['birthday']= approx_birthday.date()
        member_dict['status']='Inc'
        return member_dict
    
    def make_new_member(self):
        new_member = Member(self.return_dict())
        new_member.save()    
            
    def is_valid_id(self):
        if (len(self.id)!=8) or not self.id.isdigit(): 
            return False
        return True
    
    def get_last_name(self):
        name=self.json_inmate['nameLast']
        return name.title()
    
    def get_first_name(self):
        name=self.json_inmate['nameFirst']+" "+self.json_inmate['nameMiddle']
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
            return "2100-12-31"

    def get_csv_list(self):
        return [self.id, "%s, %s" % (self.get_last_name(), self.get_first_name()), self.json_inmate['faclName'], self.get_discharge_date(), 'N/A', 'Fed-No', 'Unk', 'FED']


# test=Fed_Member('34475018').return_dict()
# for key, value in test.iteritems():
#     print key+" : "+value