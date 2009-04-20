# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from models import Db

urlpatterns = patterns('lansite.run1s.views',
	(r'^$', 'index'),
	(r'^dbacl/(?P<db_id>\d+)/$', 'dbacl'),
	(r'^useracl/(?P<user_id>\d+)/$', 'useracl'),
)
