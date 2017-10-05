from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', home, name = 'home'),
    url(r'all$', all_orgs, name = 'all_orgs'),
    url(r'org_home/(?P<org_id>\d+)$', org_home, name = 'org_home'),
    url(r'add_org$', add_org, name = 'add_org'),
    url(r'test$', test, name = 'test'),
    url(r'modal$', modal, name = 'modal'),
    ]
