# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import databrowse
#import django.views.generic
from models import *

for m in modellist:
	databrowse.site.register(m)

info_dict = {
	'queryset': Org.objects.all(),
}
urlpatterns = patterns('lansite.sro.views',
	(r'^$', 'index'),
	(r'^org/$', 'org'),
	#(r'^org/$', 'django.views.generic.list_detail.object_list', info_dict),
	(r'^org/(?P<org_id>\d+)/main/view/$',	'org_main_view'),
	(r'^org/(?P<org_id>\d+)/main/edit/$',	'org_main_edit'),
	(r'^org/(?P<org_id>\d+)/okved/edit/$',	'org_okved_edit'),
	(r'^org/(?P<org_id>\d+)/phone/edit/$',	'org_phone_edit'),
	(r'^org/(?P<org_id>\d+)/email/edit/$',	'org_email_edit'),
	(r'^org/(?P<org_id>\d+)/sro/view/$',	'org_sro_view'),
	(r'^org/(?P<org_id>\d+)/stuff/view/$',	'org_stuff_view'),
	(r'^org/(?P<org_id>\d+)/files/view/$',	'org_files_view'),
	(r'^org/(?P<org_id>\d+)/event/view/$',	'org_events_view'),
	(r'^org/(?P<org_id>\d+)/del/$', 'org_del'),
	(r'^org/add/$', 'org_add'),
	(r'^person/$', 'person'),
	(r'^meeting/$', 'meeting'),
	(r'^export/$', 'exportxml'),
	(r'^import/$', 'importxml'),
	(r'^myexport/$', 'exml'),
	(r'^myimport/$', 'ixml'),
	(r'^delete/$', 'deleteall'),
	(r'^databrowse/(.*)', databrowse.site.root),
)
