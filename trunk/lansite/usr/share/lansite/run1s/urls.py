# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from models import Db

urlpatterns = patterns('lansite.run1s.views',
	(r'^$', 'index'),
	(r'^dbacl/(?P<db_id>\d+)/$', 'dbacl'),
	(r'^dbacldel/(?P<user_id>\d+)/(?P<db_id>\d+)/$', 'dbacldel'),
	(r'^useracl/(?P<user_id>\d+)/$', 'useracl'),
	(r'^useracldel/(?P<user_id>\d+)/(?P<db_id>\d+)/$', 'useracldel'),
	(r'^sn/$', 'sn'),
	(r'^listxml/(?P<login>\w+)/(?P<password>\w+)/$', 'listxml'),
	(r'^listtxt/(?P<login>\w+)/(?P<password>\w+)/$', 'listtxt'),
	(r'^import/$', 'importdb'),
)
