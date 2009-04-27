# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from models import Db

urlpatterns = patterns('lansite.sro.views',
	(r'^$', 'index'),
	(r'^dbacl/(?P<db_id>\d+)/$', 'dbacl'),
	(r'^dbacldel/(?P<user_id>\d+)/(?P<db_id>\d+)/$', 'dbacldel'),
	(r'^useracl/(?P<user_id>\d+)/$', 'useracl'),
	(r'^useracldel/(?P<user_id>\d+)/(?P<db_id>\d+)/$', 'useracldel'),
	(r'^import/$', 'importdb'),
)
