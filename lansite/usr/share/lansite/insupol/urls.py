# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import databrowse
#from models import Db
from models import *

for m in modellist:
	databrowse.site.register(m)

urlpatterns = patterns('lansite.insupol.views',
	(r'^$', 'index'),
	(r'^databrowse/(.*)', databrowse.site.root),
)
