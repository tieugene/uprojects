# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings

admin.autodiscover()

from views import index

urlpatterns = patterns('',
	(r'^$', index),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/(.*)', admin.site.root),
	(r'^login/$', login),
	(r'^logout/$', logout),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
#	(r'^gw/', include('lansite.gw.urls')),
#	(r'^insupol/', include('lansite.insupol.urls')),
#	(r'^run1s/', include('lansite.run1s.urls')),
#	(r'^sro/', include('sro.urls')),
#	(r'^sro2/', include('sro2.urls')),
#	(r'^todo/', include('todo.urls')),
	(r'^kladr/', include('kladr.urls')),
)
