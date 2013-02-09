from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index', name='index'),
    url(r'^patient/', include('patient.urls')),
    url(r'^employee/', include('employee.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^ref/', include('ref.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'django.contrib.auth.views.login'),
    url(r'^logout$', 'django.contrib.auth.views.logout'),
)
