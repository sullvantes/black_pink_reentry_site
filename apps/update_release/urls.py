from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', home, name = 'home'),
    url(r'^ind_search$', ind_search, name = 'ind_search'),
    url(r'^results$', results, name = 'results'),
    url(r'^results_hidden$', results_hidden, name = 'results_hidden'),
    
]