from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', home, name = 'home'),
    url(r'add_members$', add_members, name = 'add_members'),
    url(r'show$', show, name = 'show'),
#    updates members searched recently
    url(r'update/existing$', update_existing, name = 'update_existing'), 
#    updates saved members
    url(r'update/searched$', update_searched, name = 'update_searched'),

#    url(r'(?P<gov_id>\d+)$', member_home, name = 'member_home'),
    

    ]
