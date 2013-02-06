from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$',                          views.index, name='core_index'),
    url(r'^person/$',                   views.person_list, name='person_list'),
    url(r'^person/c/$',	                views.person_create, name='person_create'),
    url(r'^person/(?P<id>\d+)/r/$',	    views.person_detail, name='person_detail'),
    url(r'^person/(?P<id>\d+)/sd/$',	views.person_delete, name='person_delete'),
    url(r'^person/(?P<id>\d+)/um/$',    views.person_update_main, name='person_update_main'),
)
