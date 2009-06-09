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

def	index(request):
	return render_to_response('insupol/index.html')

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
