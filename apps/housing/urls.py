from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', home, name = 'home'),
    url(r'^search$', search, name = 'search'),
    url(r'^results$', results, name = 'results'),
    ]
