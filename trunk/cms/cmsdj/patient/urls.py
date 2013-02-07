from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$',                      views.index, name='patient_index'),
    url(r'^patient/$',              views.patient_list, name='patient_list'),
    url(r'^patient/(?P<id>\d+)/$',	views.patient_detail, name='patient_detail'),
)
