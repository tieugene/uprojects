# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^lansite/', include('lansite.foo.urls')),
	(r'^run1s/', include('lansite.run1s.urls')),
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' to INSTALLED_APPS to enable admin documentation:
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),
)
