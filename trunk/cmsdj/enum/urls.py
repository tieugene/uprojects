from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', 'enum.views.index', name='enum_index'),
    url(r'^gender/$', 'enum.views.gender_list', name='gender_list'),
    url(r'^gender/(?P<id>\d+)/$',	   views.gender_detail, name='gender_detail'),
)
