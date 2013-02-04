from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', 'core.views.index', name='core_index'),
    url(r'^person/$', 'core.views.person_list', name='person_list'),
    url(r'^person/(?P<id>\d+)/$',	   views.person_detail, name='person_detail'),
)
