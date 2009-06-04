# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from lansite.views import index
from lansite.sro.views import dl_file

urlpatterns = patterns('',
	(r'^$', index),
	(r'^run1s/', include('lansite.run1s.urls')),
	(r'^sro/', include('lansite.sro.urls')),
	(r'^admin/sro/file/(\d+)/(\d+)$', dl_file),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)', admin.site.root),
)
