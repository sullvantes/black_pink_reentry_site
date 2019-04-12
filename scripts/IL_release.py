from __future__ import unicode_literals

import codecs

import os
import re
import shutil
import requests as url_requests
from bs4 import BeautifulSoup
from datetime import datetime

# from django.db import models
# from django import forms
# from django.forms import ModelForm
# from django.contrib.auth.models import User

# from models import Facility
# from ..manage_member.models import *

IL_url = 'http://www.idoc.state.il.us/subsections/search/inms_print.asp?idoc='

class Ill_Member(object):
    def __init__(self,id):
        self.id = id
        self.msr = False
        self.life = False
        self.errors=[]
        self.soup = self.get_soup()
        self.create_values()

    def get_soup(self):
        full_url = IL_url + self.id
        response = url_requests.get(full_url)
        return BeautifulSoup(response.text, "html.parser")

    def create_values(self):
        self.inc = self.incarcerated()
        if self.inc:
            self.so = self.sex_offense()
            self.status = self.get_status()
            if self.status != 'Inc':
                self.fac_name = "Free World?"
            else:
                self.fac_name= self.get_facility_name()
            self.get_name()
            self.dob=self.get_dob()
            self.inc_date = self.get_inc_date()
            self.par_date = self.get_parole_date()
            self.dis_date = self.get_discharge_date()


    def return_dict(self):
        member_dict={}
        member_dict['gov_id']=self.id
        member_dict['status']=self.status()
        if self.inc():
            member_dict['first_name'] = self.first_name
            member_dict['last_name'] = self.last_name
            member_dict['incarcerated_date'] = self.inc_date
            member_dict['birth_date'] = self.dob
            member_dict['parole_date'] = self.par_date
            member_dict['status'] = self.status
            if member_dict['status'] == "Par":
                member_dict['facility_name'] = "Free World"
                member_dict['discharge_date'] = None
            else:
                member_dict['facility_name'] = self.fac_name
                member_dict['discharge_date'] = self.dis_date
                member_dict['msr'] = self.msr
                member_dict['life'] = self.life
            member_dict['typestate'] = 'IL'
            member_dict['so'] = self.so
        return member_dict

    def make_new_member(self):
        new_member = Member(
                    gov_id = self.id,
                    given_name = self.get_name(),
                    given_name_alpha = self.get_alpha_name(),
                    birth_date=self.get_dob(),
                    incarcerated_date=self.get_inc_date(),
                    parole_date=self.get_parole_date(),
                    so=self.get_so(),
                    status=self.get_status(),
                        )
        if d_date:
            new_member.discharge_date=d_date

    def incarcerated(self):
        return not bool(len(self.soup.findAll(text='Inmate NOT found')))

    def sex_offense(self):
        return bool(len(self.soup.findAll('td', text='Sex Offender Registry Required')))

    def get_status(self):
        if self.inc:
            status_text = self.soup.find(string="Offender Status: ").find_next('td').string
            if 'IN CUSTODY' in status_text:
                return 'Inc'
            if 'PAROLE' in status_text or not self.incarcerated():
                return 'Par'
            return 'Unknown'
        else:
            return 'Unknown'

    def get_name(self):
        try:
            name_div = self.soup.find(string="Parent Institution: ").find_previous('div').string
            name = re.findall(r"[\w']+", name_div)
            self.first_name = name[2]
            self.last_name = name[1]
        except:
            self.errors += "name"
            self.first_name = ''
            self.last_name = ''

    def get_facility_name(self):
        try:
           x = self.soup.find(string="Parent Institution: ").find_next('td').string
           return x
        except Exception as inst:
            self.errors += "Error finding Prison"
            return "Error finding Prison"


    def make_datetime(self, date_str):
        try:
            timestr=datetime.strptime(date_str, '%m/%d/%Y').date()
        except:
            timestr=date_str
        return timestr

    def get_dob(self):
        dob = self.soup.find(string="Date of Birth: ").find_next('td').string
        return self.make_datetime(dob)

    def get_inc_date(self):
        inc = self.soup.find(string="Admission Date: ").find_next('td').string
        return self.make_datetime(inc)

        # inc_date=self.get_item('Admission Date: ',10)
        # return self.make_datetime(inc_date)

    def get_parole_date(self):
        try:
            if self.get_status() == "Par":
                par = self.soup.find(string="Parole Date: ").find_next('td').string
            else:
                par = self.soup.find(string="Projected Parole Date: ").find_next('td').string
        except:
            par="No Parole"
        return self.make_datetime(par)

    def get_discharge_date(self):
        # dis_date=self.get_item('Projected Discharge Date: ',10)
        dis_date = self.soup.find(string="Projected Discharge Date: ").find_next('td').string
        if '3 YRS TO LIFE' in dis_date:
            self.msr=True
        if 'INELIGIBLE' in dis_date or 'SEXUALLY D' in dis_date:
            self.life=True
        return self.make_datetime(dis_date)

    def get_csv_list(self):
        if self.incarcerated():
            return [self.id, "%s, %s" % (self.last_name, self.first_name), self.fac_name, self.dis_date,
                    self.par_date, self.life, self.so, self.msr]
        else:
            return [self.id, "Member ID not found. Probably been discharged without parole or the member ID is in error"]
    # def get_name(self):
    #
    # # name = self.get_alpha_name().split(',')
    # #     return name[1], name[0]
    #
    # def cut_soup(self):
    #     soup_string = self.get_soup()
    #     type(soup_string)
    #     start_index = soup_string.find(self.cut_beginning)
    #     end_index = soup_string.find(self.cut_end)
    #     return soup_string[start_index:end_index]
    #
    # def get_item(self, beginning, end):
    #     beginning_index = self.cut_soup().find(beginning) + len(beginning)
    #
    #     if type(end) is int:
    #         end_index = beginning_index + end
    #     else:
    #         sub_soup = self.cut_soup()[beginning_index:]
    #         item_length = sub_soup.find(end)
    #         end_index = beginning_index + item_length
    #
    #     item = self.cut_soup()[beginning_index:end_index].strip()
    #     return item


# test_mem = Ill_Member('R75586')
# print test_mem.return_dict()
# test_mem2 = Ill_Member('R36087')
# print test_mem2.return_dict()
# test_mem3 = Ill_Member('xxxxxx')
# print test_mem3.return_dict()


def make_csv(list):
    for id in ids:
        print Ill_Member(id)

if __name__ == '__main__':
    Test_IL()