# -*- coding: utf-8 -*-
'''
KLADR views
'''
# 1. django
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context, RequestContext
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
# 2. other python
# 3. my
from models import *
from forms import *
#from dbf_imp import imp_all
import settings
import dbf_ro

DBF_DIR = os.path.join( settings.MEDIA_ROOT, 'KLADR' )

def	index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('../login/?next=%s' % request.path)
	return render_to_response('kladr/index.html', context_instance=RequestContext(request))

def	__calc_level( code ):
	'''mask: SSRRRGGGPPP'''
	if code[8:11] != '000': return 4
	if code[5:8]  != '000': return 3
	if code[2:5]  != '000': return 2
	return 1

def	__calc_parent( code, level ):
	'''mask: SSRRRGGGPPP'''
	if code[8:11] != '000': return 4
	if code[5:8]  != '000': return 3
	if code[2:5]  != '000': return 2
	return 1

@transaction.commit_manually
def	reset(request):
	#if (True):
	try:
		# 0. statetype
		state = list()
		StateType.objects.all().delete()
		state.append(StateType(id=1, comments=u'Центр района'))
		state.append(StateType(id=2, comments=u'Центр региона'))
		state.append(StateType(id=3, comments=u'Центр района и региона'))
		state.append(StateType(id=4, comments=u'Центральный район'))
		state[0].save()
		state[1].save()
		state[2].save()
		state[3].save()
		# 1. socr
		rd = dbf_ro.dbfreader( open(os.path.join( DBF_DIR, 'SOCRBASE.DBF' ), 'rb') )
		fields, type = rd.next(), rd.next()
		Short.objects.all().delete()
		short = dict()
		for dbf_row in rd:
			r = [ unicode( r, 'cp866' ).strip() for r in dbf_row ]
			if (not Short.objects.filter(name=r[1])):
				short[r[1]] = Short(name=r[1], fullname=r[2])
				short[r[1]].save()
		rd.close()
		# 2. kladr
		rd = dbf_ro.dbfreader( open(os.path.join( DBF_DIR, 'KLADR.DBF' ), 'rb') )
		fields, type = rd.next(), rd.next()
		Kladr.objects.all().delete()
		for dbf_row in rd:
			r = [ unicode( r, 'cp866' ).strip() for r in dbf_row ]
			if ((r[2][11:]) == '00'):			# actual
				l = __calc_level(r[2])
				istate = int(r[7])
				s = state[istate - 1] if istate else None
				zip = int(r[3]) if (r[3]) else None
				# TODO: parent
				Kladr(
					id = long(r[2] + '00'),		# pad to 15-digit for street compatibility
					name = r[0],
					short = short[r[1]],
					level = l,
					zip = zip,
					okato = r[6],
					center = s
				).save()
		rd.close()
	except:
		transaction.rollback()
	else:
		transaction.commit()
	# 3. street
	return render_to_response('kladr/dummy.html', context_instance=RequestContext(request))

def	update(request):
	return render_to_response('kladr/dummy.html', context_instance=RequestContext(request))
