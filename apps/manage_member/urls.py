from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', home, name = 'home'),
    url(r'add_members$', add_members, name = 'add_members'),
    url(r'show$', show, name = 'show'),
    url(r'show_updated$', show_by_updated, name = 'show_by_updated'),
    url(r'show_stale$', show_stale, name = 'show_stale'),
    url(r'show_months$', show_months, name = 'show_months'),
    url(r'update/(?P<num>\d+)$', update, name = 'update'), 
#    updates members searched recently
    url(r'update/existing$', update_existing, name = 'update_existing'), 
#    updates saved members
    url(r'update/searched$', update_searched, name = 'update_searched'),
    url(r'update/by_id/(?P<id>\d+)$$', update_by_id, name = 'update_by_id'),
    url(r'csv_print$', csv_print, name = 'csv_print'),
#    url(r'(?P<gov_id>\d+)$', member_home, name = 'member_home'),
    

    ]
