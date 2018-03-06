from django.conf.urls import url
from views import *

urlpatterns = [
    # url(r'^$', home, name = 'home'),
    url(r'^login$', login, name = 'login'),
    # url(r'^authenticate$', authenticate, name = 'authenticate'),
    # url(r'^register$', register, name = 'register'),
    # url(r'^create_user$', create_user, name = 'create_user'),
    # url(r'^new_user_success$', new_user_success, name = 'new_user_success'),
    url(r'^logout$', logout, name = 'logout'),
    ]
