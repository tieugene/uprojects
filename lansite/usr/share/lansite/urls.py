# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings

admin.autodiscover()

from lansite.views import index

urlpatterns = patterns('',
	(r'^$', index),
#	(r'^run1s/', include('lansite.run1s.urls')),
	(r'^sro/', include('lansite.sro.urls')),
	(r'^sro2/', include('lansite.sro2.urls')),
#	(r'^insupol/', include('lansite.insupol.urls')),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)', admin.site.root),
	(r'^login/$', login),
	(r'^logout/$', logout),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
)
