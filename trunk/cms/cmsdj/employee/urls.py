from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', 'employee.views.index', name='employee_index'),
    url(r'^employee/$', 'employee.views.employee_list', name='employee_list'),
    url(r'^employee/(?P<id>\d+)/$',	   views.employee_detail, name='employee_detail'),
)
