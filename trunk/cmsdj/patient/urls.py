from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^patient/$',                  views.patient_list, name='patient_list'),
    url(r'^patient/(?P<id>\d+)/$',	    views.patient_detail, name='patient_detail'),
    url(r'^patient/c/$',	            views.patient_create, name='patient_create'),
    url(r'^patient/(?P<id>\d+)/u/$',	views.patient_update, name='patient_update'),
    url(r'^patient/(?P<id>\d+)/d/$',	views.patient_delete, name='patient_delete'),
)
