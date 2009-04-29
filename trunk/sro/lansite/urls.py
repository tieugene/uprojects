# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from lansite.views import index

urlpatterns = patterns('',
	# Example:
	# (r'^lansite/', include('lansite.foo.urls')),
	(r'^$', index),
	(r'^sro/', include('lansite.sro.urls')),
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' to INSTALLED_APPS to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),
)
