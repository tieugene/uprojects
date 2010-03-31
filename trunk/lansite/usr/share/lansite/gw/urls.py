# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('lansite.gw.views',
	(r'^$',					'index'),

	(r'^task/list/$',			'task_list'),

	(r'^todoc/list/$',			'todocat_list'),
	(r'^todoc/add/$',			'todocat_add'),
	(r'^todoc/view/(?P<item_id>\d+)/$',	'todocat_view'),
	(r'^todoc/edit/(?P<item_id>\d+)/$',	'todocat_edit'),
	(r'^todoc/del/(?P<item_id>\d+)/$',	'todocat_del'),

	(r'^todo/list/$',			'todo_list'),
	(r'^todo/add/$',			'todo_add'),
	(r'^todo/view/(?P<item_id>\d+)/$',	'todo_view'),
	(r'^todo/edit/(?P<item_id>\d+)/$',	'todo_edit'),
	(r'^todo/del/(?P<item_id>\d+)/$',	'todo_del'),
#	(r'^todo/addsub/(?P<item_id>\d+)/$',	'todo_addsub'),
#	(r'^todo/onsub/(?P<item_id>\d+)/$',	'todo_onsub'),
#	(r'^todo/unsub/(?P<item_id>\d+)/$',	'todo_unsub'),

	(r'^assignc/list/$',			'assigncat_list'),
	(r'^assignc/add/$',			'assigncat_add'),
	(r'^assignc/view/(?P<item_id>\d+)/$',	'assigncat_view'),
	(r'^assignc/edit/(?P<item_id>\d+)/$',	'assigncat_edit'),
	(r'^assignc/del/(?P<item_id>\d+)/$',	'assigncat_del'),

	(r'^t/list/$',				'assign_list'),
	(r'^t/add/$',				'assign_add'),
	(r'^t/view/(?P<item_id>\d+)/$',		'assign_view'),
	(r'^t/edit/(?P<item_id>\d+)/$',		'assign_edit'),
	(r'^t/del/(?P<item_id>\d+)/$',		'assign_del'),
	(r'^t/route/(?P<item_id>\d+)/$',	'assign_route'),
	(r'^t/invalid/(?P<item_id>\d+)/$',	'assign_invalid'),
	(r'^t/duped/(?P<item_id>\d+)/$',	'assign_duped'),
	(r'^t/accept/(?P<item_id>\d+)/$',	'assign_accept'),
	(r'^t/done/(?P<item_id>\d+)/$',		'assign_done'),
	(r'^t/approve/(?P<item_id>\d+)/$',	'assign_approve'),
	(r'^t/reopen/(?P<item_id>\d+)/$',	'assign_reopen'),
	(r'^t/mkdep/(?P<item_id>\d+)/$',	'assign_mkdep'),
)