# -*- coding: utf-8 -*-
'''
SRO2 URLs
'''
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
#import django.views.generic
from models import *

urlpatterns = patterns('kladr.views',
	(r'^$',				'index'),
	(r'^view/(?P<item_id>\d+)/$',	'view'),
)
