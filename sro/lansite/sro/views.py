# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.db import transaction
from django.core import serializers
from xml.sax import handler, make_parser

import pprint

from models import *
from forms import *

modellist = (Okopf, Okved, Okso, Skill, Okdp, Stage, StageOkdp, StageOkso, Phone, Email, File, EventType, Role, Person, PersonSkill, PersonFile, Org, OrgOkved, OrgLOkdp, OrgSOkdp, OrgPhone, OrgEmail, OrgEvent, OrgStuff, OrgFile, Meeting, MeetingOrg)

def     index(request):
	return render_to_response('sro/index.html')

def	exportxml(request):
	response = HttpResponse(mimetype='text/xml; charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename=sro.xml'
	xml_serializer = serializers.get_serializer("xml")()
	data = ''
	l = list()
	for i in modellist:
		l += list(i.objects.all())
	data += xml_serializer.serialize(l)
	response.write(data)
	return response

def	exml(request):
	response = HttpResponse(mimetype='text/xml; charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename=sro.xml'
	response.write('<?xml version="1.0" encoding="utf-8"?>\n')
	response.write('<sroxml version="1.0">\n')
	for m in (Okopf, Okved, Okso, Skill, Okdp):
		response.write(u'<%s>\n' % m.xmlname)
		for i in m.objects.all():
			response.write(i.exml())
		response.write(u'</%s>\n' % m.xmlname)
	response.write('</sroxml>\n')
	return response

@transaction.commit_manually
def	importxml(request):
	if (request.method == 'POST'):
		form = ImportForm(request.POST, request.FILES)
		if form.is_valid():
		#if (True):
			file = request.FILES['file']
			if (file):
				try:
					for obj in modellist:
						obj.objects.all().delete()
					for obj in serializers.deserialize("xml", file):
						obj.save()
				except:
					transaction.rollback()
					print "Error importing transaction"
				else:
					transaction.commit()
			else:
				print "Not file"
		else:
			print "Invalid form"
	return HttpResponseRedirect('/sro/')

class	ImpHandler(handler.ContentHandler): 
	def startElement(self, name, a):
		if (name == 'okopf'):
			Okopf(id=int(a['id']), name=a['name'], shortname=a.get('shortname', None), disabled=a.get('disabled', False), parent=a.get('parent', None)).save()
	def endElement(self, name):
		if name == 'okopfs':
			pass

def	parsexml(file):
	print 'trying parse'
	handler = ImpHandler()
	parser = make_parser()
	parser.setContentHandler(handler)
	parser.parse(file)

@transaction.commit_manually
def	ixml(request):
	if (request.method == 'POST'):
		form = ImportForm(request.POST, request.FILES)
		if form.is_valid():
		#if (True):
			file = request.FILES['file']
			if (file):
				try:
					print 'start deleting...'
					for obj in modellist:
						obj.objects.all().delete()
					print 'end deleting...'
					parsexml(file)
				except:
					transaction.rollback()
					print "Error importing transaction"
				else:
					transaction.commit()
			else:
				print "Not file"
		else:
			print "Invalid form"
	return HttpResponseRedirect('/sro/')

@transaction.commit_manually
def	deleteall(request):
#	for obj in modellist:
#		obj.objects.all().delete()
	try:
		for obj in modellist:
			obj.objects.all().delete()
	except:
		transaction.rollback()
		print "Error deleting all transaction"
	else:
		transaction.commit()
	return HttpResponseRedirect('/sro/')
