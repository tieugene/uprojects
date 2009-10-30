# -*- coding: utf-8 -*-
'''
SRO URLs
'''
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib.auth.views import login, logout
#import django.views.generic
from models import *

for m in modellist:
	databrowse.site.register(m)

info_dict = {
	'queryset': Org.objects.all(),
}
urlpatterns = patterns('lansite.sro.views',
	(r'^$', 'index'),
	#(r'^org/$', 'django.views.generic.list_detail.object_list', info_dict),
	(r'^org/$',							'org_list'),
	(r'^org_i/(?P<id>\d+)/$',					'org_list_insurer'),
	(r'^org_o/(?P<id>\d+)/$',					'org_list_okato'),
	(r'^org/publish/$',						'org_publish'),
	(r'^org/upload/$',						'org_upload'),
	(r'^org/(?P<org_id>\d+)/$',					'org_view'),
	(r'^org/(?P<org_id>\d+)/edit/main/$',				'org_edit_main'),
	(r'^org/(?P<org_id>\d+)/license/add/$',				'org_license_add'),
	(r'^org/(?P<org_id>\d+)/license/edit/$',			'org_license_edit'),
	(r'^org/(?P<org_id>\d+)/license/del/$',				'org_license_del'),
	(r'^org/(?P<org_id>\d+)/insurance/add/$',			'org_insurance_add'),
	(r'^org/(?P<org_id>\d+)/insurance/edit/$',			'org_insurance_edit'),
	(r'^org/(?P<org_id>\d+)/insurance/del/$',			'org_insurance_del'),
	(r'^org/(?P<org_id>\d+)/edit/okved/$',				'org_edit_okved'),
	(r'^org/(?P<org_id>\d+)/edit/okved/(?P<item_id>\d+)/del/$',	'org_edit_okved_del'),
	(r'^org/(?P<org_id>\d+)/edit/phone/$',				'org_edit_phone'),
	(r'^org/(?P<org_id>\d+)/edit/phone/(?P<item_id>\d+)/del/$',	'org_edit_phone_del'),
	(r'^org/(?P<org_id>\d+)/edit/email/$',				'org_edit_email'),
	(r'^org/(?P<org_id>\d+)/edit/email/(?P<item_id>\d+)/del/$',	'org_edit_email_del'),
	(r'^org/(?P<org_id>\d+)/edit/www/$',				'org_edit_www'),
	(r'^org/(?P<org_id>\d+)/edit/www/(?P<item_id>\d+)/del/$',	'org_edit_www_del'),
	(r'^org/(?P<org_id>\d+)/edit/stuff/$',				'org_edit_stuff'),
	(r'^org/(?P<org_id>\d+)/edit/stuff/add_person/$',		'org_edit_stuff_add_person'),
	(r'^org/(?P<org_id>\d+)/edit/stuff/add_role/$',			'org_edit_stuff_add_role'),
	(r'^org/(?P<org_id>\d+)/edit/stuff/(?P<item_id>\d+)/del/$',	'org_edit_stuff_del'),
	(r'^org/(?P<org_id>\d+)/edit/permit/$',				'org_edit_permit'),
	(r'^org/(?P<org_id>\d+)/edit/permit/(?P<item_id>\d+)/del/$',	'org_edit_permit_del'),
	(r'^org/(?P<org_id>\d+)/edit/event/$',				'org_edit_event'),
	(r'^org/(?P<org_id>\d+)/edit/event/(?P<item_id>\d+)/del/$',	'org_edit_event_del'),
	(r'^org/(?P<org_id>\d+)/edit/file/$',				'org_edit_file'),
	(r'^org/(?P<org_id>\d+)/edit/file/(?P<item_id>\d+)/del/$',	'org_edit_file_del'),
	(r'^org/(?P<org_id>\d+)/del/$',					'org_del'),
	(r'^org/add/$',							'org_add'),
	(r'^permit/(?P<perm_id>\d+)/$',					'permit_list'),
	(r'^permit/(?P<perm_id>\d+)/edit/$',				'permit_edit'),
	(r'^permit/(?P<perm_id>\d+)/html/$',				'permit_html'),
	(r'^permit/(?P<perm_id>\d+)/pdf/$',				'permit_pdf'),
	(r'^permit/(?P<perm_id>\d+)/(?P<stage_id>\d+)/edit/$',		'permit_edit_stage'),
	(r'^person/$', 							'person_list'),
	(r'^person/(?P<person_id>\d+)/del/$',				'person_del'),
	(r'^person/(?P<person_id>\d+)/$',				'person_view'),
	(r'^person/(?P<person_id>\d+)/main/$',				'person_main'),
	(r'^person/(?P<person_id>\d+)/skill/$',				'person_skill'),
	(r'^person/(?P<person_id>\d+)/skill/add_speciality/$',		'person_skill_add_speciality'),
	(r'^person/(?P<person_id>\d+)/skill/add_skill/$',		'person_skill_add_skill'),
	(r'^person/(?P<person_id>\d+)/skill/(?P<item_id>\d+)/del/$',	'person_skill_del'),
	(r'^meeting/$', 'meeting'),
	(r'^importcsv/$', 'importcsv'),
	(r'^export/$', 'exportxml'),
	(r'^import/$', 'importxml'),
	(r'^myexport/$', 'exml'),
	(r'^myimport/$', 'ixml'),
	(r'^delete/$', 'deleteall'),
	(r'^databrowse/(.*)', databrowse.site.root),
#	(r'^login/$',  login),
#	(r'^logout/$', logout),
)
