from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', home, name = 'home'),
    url(r'^ind_search$', ind_search, name = 'ind_search'),
    url(r'^results$', results, name = 'results'),
    url(r'^results_hidden$', results_hidden, name = 'results_hidden'),
    url(r'^add_facility$', add_facility, name = 'add_facility'),
    url(r'^new_facility$', new_facility, name = 'new_facility'),
    url(r'^all_facilities$', all_facilities, name = 'all_facilities'),
    url(r'facility_home/(?P<facility_id>\d+)$', facility_home, name = 'facility_home'),
    
#    url(r'^pdf_print$', pdf_print, name = 'pdf_print'),
    url(r'^csv_print$', csv_print, name = 'csv_print'),
    
]