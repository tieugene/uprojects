# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from lansite.views import index
from lansite.sro.views import dl_file

urlpatterns = patterns('',
	# Example:
	# (r'^lansite/', include('lansite.foo.urls')),
	(r'^$', index),
	(r'^sro/', include('lansite.sro.urls')),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/sro/file/(\d+)/(\d+)$', dl_file),
	(r'^admin/(.*)', admin.site.root),
)
