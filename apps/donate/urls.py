from django.conf.urls import url

from views import DonateHomeView

urlpatterns = [
    url(r'^$', DonateHomeView.as_view(), name='home'),
]