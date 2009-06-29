# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.db import transaction
from django.core import serializers
from xml.sax import handler, make_parser
from datetime import datetime

from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str

import pprint

from models import *
from forms import *
from impex import *

def	index(request):
	return render_to_response('sro/index.html')

def	dl_file(request, file_id, file_name):
	'''
	web.header("Content-Type", "%s/%s;" % (item.mime_media, item.mime_type))
	web.header("Content-Transfer-Encoding" , "binary");
	web.header("Content-Disposition", "attachment; filename=\"%s\";" % item.origfn);
	web.header("Content-Length", "%d" % item.size);
	return open(os.path.join(config.filepath, "%08X" % (int(item.id)))).read()
	'''
	file = File.objects.get(id=int(file_id))
	#response = HttpResponse(mimetype='text/xml; charset=utf-8')
	response = HttpResponse(content_type = file.mime)
	response['Content-Transfer-Encoding'] = 'binary'
	# FIXME: django.http.__init__.py: ..._convert_to_ascii: value.encode('us-ascii') -> 'utf-8'
	response['Content-Disposition'] = u'attachment; filename=\"%s\";' % file.name
	response['Content-Length'] = u'%d;' % file.file.size;
	response.write(open(file.file.path).read())
	return response

def	org(request):
	org_list = Org.objects.all().order_by('id')
	return render_to_response('sro/org_list.html', {'org_list': org_list})

def	org_main_view(request, org_id):
	org = Org.objects.get(pk=org_id)
	return render_to_response('sro/org_main_view.html', {'org': org})

def	org_main_edit(request, org_id):
	org = Org.objects.get(pk=org_id)
	okopf = Okopf.objects.all()
	# 1. handmade
	#return render_to_response('sro/org_main_edit.html', { 'org': org, 'okopf': okopf })
	# 2. form
	form = OrgMainForm(instance=org)
	return render_to_response('sro/test.html', { 'form': form, })

def	org_okved_edit(request, org_id):
	org = Org.objects.get(pk=org_id)
	okved = Okved.objects.all()
	return render_to_response('sro/org_okved_edit.html', { 'org': org, 'okved': okved })

def	org_phone_edit(request, org_id):
	org = Org.objects.get(pk=org_id)
	return render_to_response('sro/org_phone_edit.html', { 'org': org })

def	org_email_edit(request, org_id):
	org = Org.objects.get(pk=org_id)
	return render_to_response('sro/org_email_edit.html', { 'org': org })

def	org_sro_view(request, org_id):
	org = Org.objects.get(pk=org_id)
	return render_to_response('sro/org_view_sro.html', {'org': org})

def	org_stuff_view(request, org_id):
	pass

def	org_files_view(request, org_id):
	pass

def	org_events_view(request, org_id):
	pass

def	org_del(request, org_id):
	org = Org.objects.get(pk=org_id)
	return render_to_response('sro/orgedit.html', {'org': org})

def	org_add(request):
	org = Org.objects.get()
	return render_to_response('sro/orgedit.html', {'org': org})

def	person(request):
	return render_to_response('sro/dummy.html')

def	meeting(request):
	return render_to_response('sro/dummy.html')
