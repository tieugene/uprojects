# -*- coding: utf-8 -*-
'''
impex
'''

from django.db import transaction
from django.core import serializers
from xml.sax import handler, make_parser
from datetime import datetime

from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str

class	timer:
	def	__init__(self):
		self.set()
	def	set(self):
		self.start = datetime.now()
	def	get(self):
		return (datetime.now() - self.start).seconds

def	exportxml(request):
	response = HttpResponse(mimetype='text/xml; charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename=sro.xml'
	xml_serializer = serializers.get_serializer("xml")()
	data = ''
	l = list()
	#t = timer()
	for i in modellist:			# 3''
		l += list(i.objects.all())
	#print t.get()
	data += xml_serializer.serialize(l)	# 50''
	response.write(data)
	#print t.get()
	return response

def	exml(request):
	'''
	9''
	'''
	response = HttpResponse(mimetype='text/xml; charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename=sro.xml'
	response.write('<?xml version="1.0" encoding="utf-8"?>\n')
	response.write('<sroxml version="1.0">\n')
	#t = timer()
	for m in modellist:
		response.write(u'<%ss>\n' % m._xmlname)
		for i in m.objects.all():
			response.write(i.exml())
		response.write(u'</%ss>\n' % m._xmlname)
	response.write('</sroxml>\n')
	#print t.get()
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

