# -*- coding: utf-8 -*-
'''
SRO2 URLs
'''
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib.auth.views import login, logout
#import django.views.generic
from models import *

for m in modellist:
	databrowse.site.register(m)

urlpatterns = patterns('sro2.views',
	(r'^$',								'index'),
	(r'^journal/$',							'journal'),
	(r'^sro/(?P<sro_id>\d+)/$',					'index_sro'),
	(r'^sro/(?P<sro_id>\d+)/list/$',				'sro_list'),
	(r'^sro/(?P<sro_id>\d+)/publish/$',				'sro_publish'),
	(r'^sro/(?P<sro_id>\d+)/upload/$',				'sro_upload'),
	(r'^sro/(?P<sro_id>\d+)/table/$',				'sro_table'),
	(r'^sro/(?P<sro_id>\d+)/mailto/$',				'sro_mailto'),
	(r'^sro/(?P<sro_id>\d+)/add/$',					'sro_org_add'),

	(r'^orgsro/(?P<orgsro_id>\d+)/$',				'orgsro_view'),
	(r'^orgsro/(?P<orgsro_id>\d+)/del/$',				'orgsro_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/org/$',				'orgsro_org_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/main/$',				'orgsro_main_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/okved/edit/$',			'orgsro_okved_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/okved/(?P<item_id>\d+)/del/$',	'orgsro_okved_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/phone/edit/$',			'orgsro_phone_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/phone/(?P<item_id>\d+)/del/$',	'orgsro_phone_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/email/edit/$',			'orgsro_email_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/email/(?P<item_id>\d+)/del/$',	'orgsro_email_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/www/edit/$',			'orgsro_www_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/www/(?P<item_id>\d+)/del/$',	'orgsro_www_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stuff/edit/$',			'orgsro_stuff_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stuff/add_person/$',		'orgsro_stuff_add_person'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stuff/add_role/$',		'orgsro_stuff_add_role'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stuff/(?P<item_id>\d+)/del/$',	'orgsro_stuff_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/cetrificate/$',			'orgsro_certificate'),
	(r'^orgsro/(?P<orgsro_id>\d+)/extract/$',			'orgsro_extract'),
	(r'^orgsro/(?P<orgsro_id>\d+)/license/add/$',			'orgsro_license_add'),
	(r'^orgsro/(?P<orgsro_id>\d+)/license/edit/$',			'orgsro_license_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/license/del/$',			'orgsro_license_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/insurance/add/$',			'orgsro_insurance_add'),
	(r'^orgsro/(?P<orgsro_id>\d+)/insurance/edit/$',		'orgsro_insurance_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/insurance/del/$',			'orgsro_insurance_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stagelist/edit/$',			'orgsro_stagelist_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stagelist/(?P<item_id>\d+)/setdefault/$',	'orgsro_stagelist_setdefault'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stagelist/resetdefault/$',	'orgsro_stagelist_resetdefault'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stagelist/(?P<type_id>\d+)/add/$',	'orgsro_stagelist_add'),
	(r'^orgsro/(?P<orgsro_id>\d+)/stagelist/(?P<item_id>\d+)/del/$',	'orgsro_stagelist_del'),
	(r'^orgsro/(?P<orgsro_id>\d+)/event/edit/$',			'orgsro_event_edit'),
	(r'^orgsro/(?P<orgsro_id>\d+)/event/(?P<item_id>\d+)/del/$',	'orgsro_event_del'),

	(r'^sro/(?P<sro_id>\d+)/person/$', 							'person_list'),
	(r'^sro/(?P<sro_id>\d+)/person/(?P<person_id>\d+)/del/$',				'person_del'),
	(r'^sro/(?P<sro_id>\d+)/person/(?P<person_id>\d+)/$',					'person_view'),
	(r'^sro/(?P<sro_id>\d+)/person/(?P<person_id>\d+)/main/$',				'person_main'),
	(r'^sro/(?P<sro_id>\d+)/person/(?P<person_id>\d+)/skill/$',				'person_skill'),
	(r'^sro/(?P<sro_id>\d+)/person/(?P<person_id>\d+)/skill/add_speciality/$',		'person_skill_add_speciality'),
	(r'^sro/(?P<sro_id>\d+)/person/(?P<person_id>\d+)/skill/add_skill/$',			'person_skill_add_skill'),
	(r'^sro/(?P<sro_id>\d+)/person/(?P<person_id>\d+)/skill/(?P<item_id>\d+)/del/$',	'person_skill_del'),

	(r'^stagelist/(?P<perm_id>\d+)/$',				'stagelist_list'),
	(r'^stagelist/(?P<perm_id>\d+)/edit/$',				'stagelist_edit'),
	(r'^stagelist/(?P<perm_id>\d+)/html/$',				'stagelist_html'),
	(r'^stagelist/(?P<perm_id>\d+)/pdf/$',				'stagelist_pdf'),
	(r'^stagelist/(?P<perm_id>\d+)/dup/$',				'stagelist_dup'),
	(r'^stagelist/(?P<perm_id>\d+)/dup/(?P<type_id>\d+)/$',		'stagelist_dup_edit'),
	(r'^stagelist/(?P<perm_id>\d+)/cmp/$',				'stagelist_cmp'),
	(r'^stagelist/(?P<perm_id>\d+)/(?P<stage_id>\d+)/edit/$',	'stagelist_edit_stage'),

	(r'^sro/(?P<sro_id>\d+)/protocol/$',				'protocol_list'),
)
