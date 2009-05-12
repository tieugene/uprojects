# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
#from models import Db

urlpatterns = patterns('lansite.sro.views',
	(r'^$', 'index'),
	(r'^export/$', 'exportxml'),
	(r'^import/$', 'importxml'),
	(r'^myexport/$', 'exml'),
	(r'^myimport/$', 'ixml'),
	(r'^delete/$', 'deleteall'),
)
