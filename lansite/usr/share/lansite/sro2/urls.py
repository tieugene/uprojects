# -*- coding: utf-8 -*-
'''
SRO URLs
'''
from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.contrib.auth.views import login, logout
#import django.views.generic
from models import *

for m in modellist:
	databrowse.site.register(m)

'''info_dict = {
	'queryset': Org.objects.all(),
}'''

urlpatterns = patterns('lansite.sro2.views',
	(r'^$', 'index'),
)
