import urllib2
import json
import re
from datetime import datetime

class Fed_Member(object):
    def __init__(self,id):
        self.id=id
        self.url = 'https://www.bop.gov/PublicInfo/execute/inmateloc?todo=query&output=json&inmateNumType=IRN&inmateNum='
        self.is_valid
        req = urllib2.Request(self.url + self.id)
        response = urllib2.urlopen(req)
        json_stats = json.load(response)
        if len(json_stats['InmateLocator']) > 1:
            self.json_inmate = json_stats['InmateLocator'][0]
        else:
            self.json_inmate = None
        print "Building",self.id,"..."

    def return_dict(self):
        print self.json_inmate
        member_dict = {}
        member_dict['Id'] = self.id
        if self.json_inmate is None:
            member_dict['Name']= "is not a valid Federal ID"
            return member_dict    
        name = (self.json_inmate['nameLast']+", "+self.json_inmate['nameFirst'] +" "+ self.json_inmate['nameMiddle'])
        name = re.sub(' +',' ', name)
        name = name.title()
        member_dict['Name']= name
        member_dict['Location']=self.json_inmate['faclName']
        try:
            discharge_date_obj = datetime.strptime(self.json_inmate['projRelDate'],'%m/%d/%Y')
            member_dict['Discharge_Date']=discharge_date_obj.strftime('%Y-%m-%d')
        except:
            member_dict['Discharge_Date']="No Date Given"
            
        member_dict['Age']=self.json_inmate['age']
        member_dict['TypeState']='FED'
        return member_dict
    
    def is_valid(self):
        if (len(self.id)!=8) or not self.id.isdigit(): 
            return False
        return True
    

# test=Fed_Member('34475018').return_dict()
# for key, value in test.iteritems():
#     print key+" : "+value