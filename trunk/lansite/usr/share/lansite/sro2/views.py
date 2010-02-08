# -*- coding: utf-8 -*-
'''
SRO2 views
'''
# 1. django
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context, RequestContext
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
# 2. other python
import ftplib, netrc, tempfile, pprint
from datetime import datetime
from trml2pdf import trml2pdf
# 3. my
from models import *
from forms import *

def	index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('../login/?next=%s' % request.path)
	return render_to_response('sro2/index.html', context_instance=RequestContext(request))
