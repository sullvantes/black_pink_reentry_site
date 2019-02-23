from __future__ import unicode_literals
import re
from bs4 import BeautifulSoup
import codecs
import shutil
import csv
import os
import urllib2
from datetime import datetime
from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

# Offender Status:	PAROLE
from models import Facility
from ..manage_member.models import *

response = urllib2.urlopen('http://python.org/')
html = response.read()


class Ill_Member(object):
    def __init__(self, id):
        self.id = id
        self.url = 'http://www.idoc.state.il.us/subsections/search/inms_print.asp?idoc='
        self.cut_beginning = self.id
        self.cut_end = "SENTENCING INFORMATION"
        self.msr = False
        self.life = False
        print "Building", self.id, "..."

    def return_dict(self):
        member_dict = {}
        member_dict['gov_id'] = self.id
        member_dict['status'] = self.get_status()
        if self.incarcerated():
            member_dict['first_name'], member_dict['last_name'] = self.get_name()
            member_dict['incarcerated_date'] = self.get_inc_date()
            member_dict['birth_date'] = self.get_dob()
            member_dict['parole_date'] = self.get_parole_date()
            member_dict['status'] = self.get_status()
            if member_dict['status'] == "Par":
                member_dict['facility_name'] = "Free World"
                member_dict['discharge_date'] = None
            else:
                member_dict['facility_name'] = self.get_facility()
                member_dict['discharge_date'] = self.get_discharge_date()
                member_dict['msr'] = self.msr
                member_dict['life'] = self.life
            member_dict['typestate'] = 'IL'
            member_dict['so'] = self.get_so()
        return member_dict

    def make_new_member(self):
        new_member = Member(
            gov_id=self.id,
            given_name=self.get_name(),
            given_name_alpha=self.get_alpha_name(),
            birth_date=self.get_dob(),
            incarcerated_date=self.get_inc_date(),
            parole_date=self.get_parole_date(),
            so=self.get_so(),
            status=self.get_status(),
        )
        if d_date:
            new_member.discharge_date = d_date

    def get_soup(self):
        full_url = self.url + self.id
        response = urllib2.urlopen(full_url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        soup_string = soup.get_text().strip()
        return soup_string

    def incarcerated(self):
        if 'Inmate NOT found' in self.get_soup():
            return False
        return True

    def cut_soup(self):
        soup_string = self.get_soup()
        type(soup_string)
        start_index = soup_string.find(self.cut_beginning)
        end_index = soup_string.find(self.cut_end)
        return soup_string[start_index:end_index]

    def get_so(self):
        if 'Sex Offender Registry Required' in self.get_soup():
            return True
        return False

    def get_item(self, beginning, end):
        beginning_index = self.cut_soup().find(beginning) + len(beginning)

        if type(end) is int:
            end_index = beginning_index + end
        else:
            sub_soup = self.cut_soup()[beginning_index:]
            item_length = sub_soup.find(end)
            end_index = beginning_index + item_length

        item = self.cut_soup()[beginning_index:end_index].strip()
        return item

    def get_status(self):
        status_text = self.get_item("Offender Status:", "Location:")
        if status_text == 'IN CUSTODY':
            return 'Inc'
        if status_text == 'PAROLE' or not self.incarcerated():
            return 'Par'
        return 'Unknown'

    def get_alpha_name(self):
        return self.get_item(self.id + " - ", "Parent Institution:").title()

    def get_name(self):
        name = self.get_alpha_name().split(',')
        return name[1], name[0]

    def get_facility(self):
        return self.get_item("Parent Institution:", "Offender Status:").title()

    def make_datetime(self, date):
        try:
            timestr = datetime.strptime(date, '%m/%d/%Y').date()
        except:
            timestr = None
        return timestr

    def get_dob(self):
        dob = self.get_item('Date of Birth: ', 10)
        return self.make_datetime(dob)

    def get_inc_date(self):
        inc_date = self.get_item('Admission Date: ', 10)
        return self.make_datetime(inc_date)

    def get_parole_date(self):
        if self.get_status() == "PAROLE":
            parole_date = self.get_item('Parole Date: ', 10)
        else:
            parole_date = self.get_item('Projected Parole Date: ', 10)
        return self.make_datetime(parole_date)

    def get_discharge_date(self):
        dis_date = self.get_item('Projected Discharge Date: ', 10)
        # print "Is This MSR?", dis_date
        if dis_date == '3 YRS TO L':
            self.msr = True
            return None
        if dis_date == 'INELIGIBLE' or dis_date == 'SEXUALLY D':
            self.life = True
            return None
        if dis_date == 'TO BE DETE':
            return None
        return self.make_datetime(dis_date)


def Test_IL(ids=['R75586']):
    for id in ids:
        print Ill_Member(id)


if __name__ == '__main__':
    Test_IL()