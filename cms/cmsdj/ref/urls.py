from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', 'ref.views.index', name='ref_index'),
    url(r'^mkb10/$', 'app1.views.mkb10_list', name='mkb10_list'),
    url(r'^mkb10/(?P<id>\d+)/$',	   views.mkb10_detail, name='mkb10_detail'),
)
