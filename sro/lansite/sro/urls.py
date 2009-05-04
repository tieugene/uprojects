# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from models import Db

urlpatterns = patterns('lansite.sro.views',
	(r'^$', 'index'),
	(r'^export/$', 'exportxml'),
	(r'^delete/$', 'deleteall'),
	(r'^import/$', 'importxml'),
)
