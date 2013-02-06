from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$',                          views.index, name='core_index'),
    url(r'^person/$',                   views.person_list, name='person_list'),
    url(r'^person/(?P<id>\d+)/r/$',	    views.person_detail, name='person_detail'),
    url(r'^person/(?P<id>\d+)/d/$',     views.person_delete, name='person_delete'),
    url(r'^person/c/$',	                views.person_create, name='person_create'),
    url(r'^person/(?P<id>\d+)/u/$',     views.person_update, name='person_update'),
    url(r'^personaddress/(?P<id>\d+)/d/$',     views.personaddress_delete, name='personaddress_delete'),
    url(r'^personaddress/(?P<id>\d+)/c/$',	   views.personaddress_create, name='personaddress_create'),
    url(r'^personaddress/(?P<id>\d+)/u/$',     views.personaddress_update, name='personaddress_update'),
)
