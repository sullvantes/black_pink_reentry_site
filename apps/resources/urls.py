from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', home, name = 'home'),
    url(r'search_types$', search_types, name = 'search_types'),
    url(r'resource_type/(?P<resource_type_id>\d+)$', resource_type, name = 'resource_type'),
    url(r'resource_list$', resource_list, name = 'resource_list'),
    url(r'view_resource/(?P<resource_id>\d+)$', view_resource, name = 'view_resource'),
    url(r'edit_resource/(?P<resource_id>\d+)$', edit_resource, name = 'edit_resource'),
    url(r'confirm_delete/(?P<resource_id>\d+)$', confirm_delete, name = 'confirm_delete'),
    url(r'delete_resource$', delete_resource, name = 'delete_resource'),
    url(r'save_resource/(?P<resource_id>\d+)$', save_resource, name = 'save_resource'),
    url(r'add_resource$', add_resource, name = 'add_resource'),
    url(r'make_list$', make_list, name = 'make_list'),
    url(r'pdf_print_resources$', pdf_print_resources, name = 'pdf_print_resources'),
    url(r'csv_print_resources$', csv_print_resources, name = 'csv_print_resources'),
    
    
    
    ]
