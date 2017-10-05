import re
from bs4 import BeautifulSoup
import codecs
import shutil
import csv
import os 
import urllib2
response = urllib2.urlopen('http://python.org/')
html = response.read()

class Ill_Member(object):
    def __init__(self,raw_id):
        self.id = re.sub('[^A-Z0-9]','', raw_id.upper())
        self.url = 'http://www.idoc.state.il.us/subsections/search/inms_print.asp?idoc='
        self.cut_beginning=self.id
        self.cut_end="SENTENCING INFORMATION"

    def return_dict(self):
        member_dict={}
        member_dict['Id']=self.id
        if self.is_valid():
            member_dict['Name']=self.get_name()
            member_dict['Location']=self.get_location()
            member_dict['DOB']=self.get_dob()
            member_dict['Parole_Date']=self.get_parole_date()
            member_dict['Incarcerated_Date']=self.get_inc_date()
            member_dict['Discharge_Date']=self.get_discharge_date()
        else:
            member_dict['Name']=self.invalid_reason

        return member_dict

    def is_valid(self):
        if (len(self.id)!=6) or not self.id[0].isalpha() or not self.id[1:].isdigit(): 
            return False
        return True
    
    def invalid_reason(self):
        if (len(self.id)!=6): 
            return " does not appear to be valid. This ID has " + str(len(self.id)) + " characters and IDOC IDs should have 6 characters."
        
        if not self.id[0].isalpha() or not self.id[1:].isdigit():
            return self.id + " does not appear to be valid. IDOC ID's have the form A12345. It may be a different state, federal or Illinois DHS."
        return None

    def get_soup(self):
        full_url = self.url + self.id
        response = urllib2.urlopen(full_url)
        html = response.read()
        soup=BeautifulSoup(html, "html.parser")
        return soup
    
    def cut_soup(self):
        soup_string = self.get_soup().get_text().strip()
        start_index = soup_string.find(self.cut_beginning)
        end_index = soup_string.find(self.cut_end)
        return soup_string[start_index:end_index]
 
    def incarcerated(self):
        if self.is_valid():
            if 'Inmate NOT found' in self.get_soup():
                return False
        return True
        
    
    def get_so(self):
        if 'Sex Offender Registry Required' in self.get_soup():
            return True
        return False

    def get_item(self,beginning,end):
    	beginning_index = self.cut_soup().find(beginning)+len(beginning)
        
        if type(end) is int:
			end_index = beginning_index+end
        else:
            sub_soup= self.cut_soup()[beginning_index:]
            item_length=sub_soup.find(end)
            end_index=beginning_index+item_length
        
        item = self.cut_soup()[beginning_index:end_index].strip()    
        return item   
    
    def get_name(self):
        return self.get_item(self.id + " - ","Parent Institution:")

    def get_location(self):
        return self.get_item("Parent Institution:","Offender Status:")

    def format_date(self,date):
        reverse_date= date[6:10]+'-'+date[0:2]+'-'+date[3:5]
        return reverse_date


    def get_dob(self):
        dob=self.get_item('Date of Birth: ',10) 
        return self.format_date(dob)

    def get_inc_date(self):
        dob=self.get_item('Admission Date: ',10) 
        return self.format_date(dob)

    def get_parole_date(self):
        dob=self.get_item('Projected Parole Date: ',10) 
        return self.format_date(dob)
    
    def get_discharge_date(self):
        dob=self.get_item('Projected Discharge Date: ',10) 
        return self.format_date(dob)

# test = Ill_Member('IL','R85647')
# print test.state
# print test.id
# print test.is_valid()
# print test.invalid_reason()
# print test.incarcerated()
# print test.get_so()
# print test.get_name()



# print test.get_location()
# print test.get_dob()
# print test.get_inc_date()
# print test.get_parole_date()
# print test.get_discharge_date()
# print test.return_dict()


# def search_IL(gov_id):
#     result={}
#     result["Id"]=gov_id
#     gov_id=re.sub('[^A-Z0-9]','', gov_id.upper())
#     if (len(gov_id)!=6): 
#         result["Name"] = " does not appear to be valid. This ID has " + str(len(gov_id)) + " characters and IDOC IDs should have 6 characters."
#         result["isValid"]=False
#         return result
    
#     if not gov_id[0].isalpha() or not gov_id[1:].isdigit():
#         result["Name"] = " does not appear to be valid. IDOC ID's have the form A12345. It may be a different state, federal or Illinois DHS."
#         result["isValid"]=False
#         return result
             
#     bashc = "wget --secure-protocol=TLSv1 'https://www.idoc.state.il.us/subsections/search/inms_print.asp?idoc='" + gov_id
    
#     os.system(bashc)
#     try:
# 		html=codecs.open("inms_print.asp?idoc=" + gov_id, 'r')
#     except:
# 		pass
	
#     soup=BeautifulSoup(html, "html.parser")
    
#     tail_snip="SENTENCING INFORMATION"
	
#     soup_string = soup.get_text().strip()
#     print soup_string
#     if "Sex Offender Registry Required" in soup_string:
#     	result["so"] = True
#         soup_string.replace(' Sex Offender Registry Required','')
#     else:
# 		result["so"] = False
    
#     start_index=soup_string.find(gov_id)
#     end_index=soup_string.find(tail_snip)
#     cut_soup = soup_string[start_index:end_index]
    
#     if 'Sex Offender Registry Required' in soup_string:
#         locationlast='Sex Offender Registry Required'
#     else:
#         locationlast='PHYSICAL PROFILE'

#     find_items = [
# 		{ 
# 			"first" : gov_id +' - ',
# 			"last" : 'Parent Institution:',
# 			"item" : 'Name',
#            "name" : 'Name',
# 		},
# 		{
# 			"last" : 'Offender Status',
# 			"item" : 'Parent Institution: ',
#           "name" : 'Parent_Institution',
# 		},
# 		{
# 			"last" : locationlast,
# 			"item" : 'Location: ',
#           "name" : 'Location',
		    
# 		},
# 		{
# 			"last" : 10,
# 			"item" : 'Date of Birth: ',
#           "name" : 'DOB',
# 		},
# 		{
# 			"last" : 10,
# 			"item" : 'Admission Date: ',
#           "name" : 'Incarcerated_Date',
# 		},
# 		{
# 			"last" : 10,
# 			"item" : 'Projected Parole Date: ',
#           "name" : 'Parole_Date',
# 		},
# 		{
# 			"last" : 10,
# 			"item" : 'Projected Discharge Date: ',
#             "name" : 'Discharge_Date',
# 		}
# 		]
	
#     for progress in find_items:
# 		if 'first' not in progress:
# 			cut_soup=cut_soup[cut_soup.find(progress["item"])+len(progress["item"]):]

# 		else:
# 			cut_soup=cut_soup[cut_soup.find(progress["first"])+len(progress["first"]):]
        
# 		if type(progress["last"]) is int:
# 			result[progress["name"]]=cut_soup[:progress["last"]]
# 		else:
# 			result[progress["name"]] = cut_soup[:cut_soup.find(progress["last"])]
#     result["isValid"]=True
#     return result