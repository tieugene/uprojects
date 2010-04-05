# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('lansite.gw.views',
	(r'^$',					'index'),

	(r'^task/list/$',			'task_list'),
	(r'^task/add/$',			'task_add'),
	(r'^task/view/(?P<item_id>\d+)/$',	'task_view'),
	(r'^task/edit/(?P<item_id>\d+)/$',	'task_edit'),
	(r'^task/del/(?P<item_id>\d+)/$',	'task_del'),
	(r'^task/done/(?P<item_id>\d+)/$',	'task_done'),

	(r'^todoc/add/$',			'todocat_add'),
	(r'^todoc/view/(?P<item_id>\d+)/$',	'todocat_view'),
	(r'^todoc/edit/(?P<item_id>\d+)/$',	'todocat_edit'),
	(r'^todoc/del/(?P<item_id>\d+)/$',	'todocat_del'),
	(r'^todoc/addtodo/(?P<item_id>\d+)/$',	'todocat_add_todo'),

	(r'^todo/list/$',			'todo_list'),
	(r'^todo/add/$',			'todo_add'),
	(r'^todo/view/(?P<item_id>\d+)/$',	'todo_view'),
	(r'^todo/edit/(?P<item_id>\d+)/$',	'todo_edit'),
	(r'^todo/del/(?P<item_id>\d+)/$',	'todo_del'),
	(r'^todo/done/(?P<item_id>\d+)/$',	'todo_done'),
#	(r'^todo/addsub/(?P<item_id>\d+)/$',	'todo_addsub'),
#	(r'^todo/onsub/(?P<item_id>\d+)/$',	'todo_onsub'),
#	(r'^todo/unsub/(?P<item_id>\d+)/$',	'todo_unsub'),

	(r'^assignc/add/$',			'assigncat_add'),
	(r'^assignc/view/(?P<item_id>\d+)/$',	'assigncat_view'),
	(r'^assignc/edit/(?P<item_id>\d+)/$',	'assigncat_edit'),
	(r'^assignc/del/(?P<item_id>\d+)/$',	'assigncat_del'),

	(r'^assign/list/$',				'assign_list'),
	(r'^assign/add/$',				'assign_add'),
	(r'^assign/view/(?P<item_id>\d+)/$',		'assign_view'),
	(r'^assign/edit/(?P<item_id>\d+)/$',		'assign_edit'),
	(r'^assign/del/(?P<item_id>\d+)/$',		'assign_del'),
	(r'^assign/route/(?P<item_id>\d+)/$',	'assign_route'),
	(r'^assign/invalid/(?P<item_id>\d+)/$',	'assign_invalid'),
	(r'^assign/duped/(?P<item_id>\d+)/$',	'assign_duped'),
	(r'^assign/accept/(?P<item_id>\d+)/$',	'assign_accept'),
	(r'^assign/done/(?P<item_id>\d+)/$',		'assign_done'),
	(r'^assign/approve/(?P<item_id>\d+)/$',	'assign_approve'),
	(r'^assign/reopen/(?P<item_id>\d+)/$',	'assign_reopen'),
	(r'^assign/mkdep/(?P<item_id>\d+)/$',	'assign_mkdep'),
)