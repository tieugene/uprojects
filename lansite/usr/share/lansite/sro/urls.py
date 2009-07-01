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
	(r'^org/(?P<org_id>\d+)/view/$',				'org_view'),
	(r'^org/(?P<org_id>\d+)/edit/main/$',				'org_edit_main'),
	(r'^org/(?P<org_id>\d+)/edit/okved/$',				'org_edit_okved'),
	(r'^org/(?P<org_id>\d+)/edit/okved/(?P<item_id>\d+)/del/$',	'org_edit_okved_del'),
	(r'^org/(?P<org_id>\d+)/edit/phone/$',				'org_edit_phone'),
	(r'^org/(?P<org_id>\d+)/edit/phone/(?P<item_id>\d+)/del/$',	'org_edit_phone_del'),
	(r'^org/(?P<org_id>\d+)/edit/email/$',				'org_edit_email'),
	(r'^org/(?P<org_id>\d+)/edit/email/(?P<item_id>\d+)/del/$',	'org_edit_email_del'),
	(r'^org/(?P<org_id>\d+)/edit/stuff/$',				'org_edit_stuff'),
	(r'^org/(?P<org_id>\d+)/edit/stuff/(?P<item_id>\d+)/del/$',	'org_edit_stuff_del'),
	(r'^org/(?P<org_id>\d+)/view/permit/(?P<item_id>\d+)/$',	'org_view_permit'),
	(r'^org/(?P<org_id>\d+)/edit/permit/$',				'org_edit_permit'),
	(r'^org/(?P<org_id>\d+)/edit/permit/(?P<item_id>\d+)/del/$',	'org_edit_permit_del'),
	(r'^org/(?P<org_id>\d+)/edit/event/$',				'org_edit_event'),
	(r'^org/(?P<org_id>\d+)/edit/event/(?P<item_id>\d+)/del/$',	'org_edit_event_del'),
	(r'^org/(?P<org_id>\d+)/edit/file/$',				'org_edit_file'),
	(r'^org/(?P<org_id>\d+)/edit/file/(?P<item_id>\d+)/del/$',	'org_edit_file_del'),
	(r'^org/(?P<org_id>\d+)/del/$',					'org_del'),
	(r'^org/add/$', 'org_edit_main'),
	(r'^person/$', 'person'),
	(r'^meeting/$', 'meeting'),
	(r'^export/$', 'exportxml'),
	(r'^import/$', 'importxml'),
	(r'^myexport/$', 'exml'),
	(r'^myimport/$', 'ixml'),
	(r'^delete/$', 'deleteall'),
	(r'^databrowse/(.*)', databrowse.site.root),
)