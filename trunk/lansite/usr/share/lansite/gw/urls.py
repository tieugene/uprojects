# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('lansite.gw.views',
	(r'^$', 'index'),
)