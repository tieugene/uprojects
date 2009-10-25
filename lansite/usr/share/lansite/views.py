# -*- coding: utf-8 -*-
'''
Main views
'''
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.db import transaction

def     index(request):
	#if not request.user.is_authenticated():
	#	return HttpResponseRedirect('/login/?next=%s' % request.path)
	return render_to_response('index.html', context_instance=RequestContext(request))

def	profile(request):
	return index(request)
