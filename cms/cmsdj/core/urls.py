from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$',                          views.index, name='core_index'),
    url(r'^person/$',                   views.person_list, name='person_list'),
    url(r'^person/(?P<id>\d+)/$',	    views.person_detail, name='person_detail'),
    url(r'^person/(?P<id>\d+)/d/$',     views.person_delete, name='person_delete'),
    url(r'^person/c/$',	                views.person_create, name='person_create'),
    url(r'^person/(?P<id>\d+)/u/$',     views.person_update, name='person_update'),
    # subs
    url(r'^person/(?P<id>\d+)/a/d/$',   views.person_delete_address, name='person_delete_address'),
    url(r'^person/(?P<id>\d+)/a/c/$',   views.person_create_address, name='person_create_address'),
    url(r'^person/(?P<id>\d+)/a/u/$',   views.person_update_address, name='person_update_address'),
    url(r'^person/(?P<id>\d+)/p/d/$',   views.person_delete_phone, name='person_delete_phone'),
    url(r'^person/(?P<id>\d+)/p/c/$',   views.person_create_phone, name='person_create_phone'),
    url(r'^person/(?P<id>\d+)/p/u/$',   views.person_update_phone, name='person_update_phone'),
    url(r'^person/(?P<id>\d+)/e/d/$',   views.person_delete_email, name='person_delete_email'),
    url(r'^person/(?P<id>\d+)/e/c/$',   views.person_create_email, name='person_create_email'),
    url(r'^person/(?P<id>\d+)/e/u/$',   views.person_update_email, name='person_update_email'),
    url(r'^person/(?P<id>\d+)/d/d/$',   views.person_delete_document, name='person_delete_document'),
    url(r'^person/(?P<id>\d+)/d/c/$',   views.person_create_document, name='person_create_document'),
    url(r'^person/(?P<id>\d+)/d/u/$',   views.person_update_document, name='person_update_document'),
    url(r'^person/(?P<id>\d+)/c/d/$',   views.person_delete_code, name='person_delete_code'),
    url(r'^person/(?P<id>\d+)/c/c/$',   views.person_create_code, name='person_create_code'),
    url(r'^person/(?P<id>\d+)/c/u/$',   views.person_update_code, name='person_update_code'),
)
