"""bp_reentry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin, auth

urlpatterns = [
    url(r'^', include('apps.main.urls', namespace='main')),
    url(r'^resources/', include('apps.resources.urls', namespace='resources')),
    url(r'^release/', include('apps.update_release.urls', namespace='release')),
    url(r'^members/', include('apps.manage_member.urls', namespace='members')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^rest/', include('apps.rest.urls', namespace='rest')),
    url(r'^housing/', include('apps.housing.urls', namespace='housing')),
    url(r'^donate/', include('apps.donate.urls', namespace='donate')),
    
]
