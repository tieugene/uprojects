from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$',                              views.index,            name='employee_index'),
    url(r'^stafflist/$',                    views.stafflist_list,   name='stafflist_list'),
    url(r'^stafflist/(?P<id>\d+)/$',        views.stafflist_view,   name='stafflist_view'),
    url(r'^staff/(?P<id>\d+)/add/$',        views.staff_add,        name='staff_add'),
    url(r'^staff/(?P<id>\d+)/edit/$',       views.staff_edit,       name='staff_edit'),
    url(r'^staff/(?P<id>\d+)/del/$',        views.staff_del,        name='staff_del'),
    url(r'^employee/$',                     views.employee_list,    name='employee_list'),
    url(r'^employee/(?P<id>\d+)/$',	        views.employee_view,    name='employee_view'),
)
