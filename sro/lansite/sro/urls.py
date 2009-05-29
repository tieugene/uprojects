# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import databrowse
#from models import Db
from models import *

for m in modellist:
	databrowse.site.register(m)

urlpatterns = patterns('lansite.sro.views',
	(r'^$', 'index'),
	(r'^export/$', 'exportxml'),
	(r'^import/$', 'importxml'),
	(r'^myexport/$', 'exml'),
	(r'^myimport/$', 'ixml'),
	(r'^delete/$', 'deleteall'),
	(r'^databrowse/(.*)', databrowse.site.root),
)
