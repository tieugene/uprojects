from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
#from dajaxice.core import dajaxice_autodiscover, dajaxice_config    # dajaxice

import views
admin.autodiscover()
#dajaxice_autodiscover() # dajaxice

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^patient/', include('patient.urls')),
    url(r'^employee/', include('employee.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^ref/', include('ref.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', login),
    url(r'^logout$', logout),
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),    # dajaxice
)
