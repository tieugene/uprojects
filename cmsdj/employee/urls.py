from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^stafflist/$',                                    views.stafflist_list,   name='stafflist_list'),
    url(r'^stafflist/(?P<id>\d+)/$',                        views.stafflist_view,   name='stafflist_view'),
    url(r'^staff/(?P<list_id>\d+)/(?P<spec_id>\d+)/add/$',  views.staff_add,        name='staff_add'),
    url(r'^staff/(?P<id>\d+)/edit/$',                       views.staff_edit,       name='staff_edit'),
    url(r'^staff/(?P<id>\d+)/del/$',                        views.staff_del,        name='staff_del'),
    url(r'^employee/$',                                     views.employee_list,    name='employee_list'),
    url(r'^employee/(?P<id>\d+)/$',	                        views.employee_view,    name='employee_view'),
    url(r'^rs_r/$',                                         views.rs_room_auto,     name='rs_room_auto'),
    url(r'^rs_r/(?P<rs_id>\d+)/(?P<room_id>\d+)/$',         views.rs_room,          name='rs_room'),
    url(r'^rse_r/(?P<id>\d+)/$',                            views.rse_room,         name='rse_room'),
    url(r'^rse_r/(?P<id>\d+)/del/$',                        views.rse_room_del,     name='rse_room_del'),
    url(r'^rsed_r/(?P<id>\d+)/$',                           views.rsed_room,        name='rsed_room'),
    url(r'^rsed_r/(?P<id>\d+)/del/$',                       views.rsed_room_del,    name='rsed_room_del'),
    url(r'^rs_d/$',                                         views.rs_dow_auto,      name='rs_dow_auto'),
    url(r'^rs_d/(?P<rs_id>\d+)/(?P<dow_id>\d+)/$',          views.rs_dow,           name='rs_dow'),
    url(r'^rse_d/(?P<id>\d+)/$',                            views.rse_dow,          name='rse_dow'),
    url(r'^rse_d/(?P<id>\d+)/del/$',                        views.rse_dow_del,      name='rse_dow_del'),
    url(r'^rsed_d/(?P<id>\d+)/$',                           views.rsed_dow,         name='rsed_dow'),
    url(r'^rsed_d/(?P<id>\d+)/del/$',                       views.rsed_dow_del,     name='rsed_dow_del'),
    url(r'^ticket/$',                                       views.ticket_list,      name='ticket_list'),
    url(r'^ticket/(?P<id>\d+)/$',	                        views.ticket_view,      name='ticket_view'),
    url(r'^ticket_t/$',                                     views.ticket_table_auto,name='ticket_table_auto'),
    url(r'^ticket_t/(?P<id>\d+)/(?P<date>\d{6})/$',         views.ticket_table,     name='ticket_table'),
)
