# -*- coding: utf-8 -*-
'''
impex
'''

import csv, pprint
from datetime import datetime
from xml.sax import handler, make_parser

from django.db import transaction
from django.core import serializers
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response

from forms import ImportForm
import models

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

fields = ('id', 'name', 'fullname', 'okopf', 'okopfname', 'inn', 'kpp', 'ogrn', 'laddr', 'raddr', 'bosstitle', 'bossname', 'contact', 'phones', 'emails', 'datevv', 'datekf', 'datez', 'date1', 'datenp', 'regno', 'datesvid', 'isaffil', 'activity', 'job', 'licstate', 'licno', 'licstart', 'licend', 'projlicno', 'projlicstart', 'projlicend', 'insurer', 'state', 'letters', 'svidfio', 'svidjob', 'sviddate', 'comments')

def	importcsv(request):
	if (request.method == 'POST'):
		form = ImportForm(request.POST, request.FILES)
		if form.is_valid():
		#if (True):
			file = request.FILES['file']
			if (file):
				#return render_to_response('sro/org_import.html', {'org_list': __parsecsv(file)})
				__insertcsv(__parsecsv(file))
			else:
				print "Not file"
		else:
			print "Invalid form"
	return HttpResponseRedirect('../')

def	__parsecsv(file):
	retvalue = list()
	#csvreader = csv.reader(file, delimiter="\t")
	csvreader = csv.DictReader(file, fieldnames=fields, delimiter="\t")
	csvreader.next()
	for row in csvreader:
		# 1. decode from utf
		#del row[None]
		for k in row.keys():
			if k:
				row[k] = row[k].decode('utf-8').strip()
		retvalue.append(row)
	return retvalue

#@transaction.commit_manually
def	__insertcsv(datalist):
	models.Org.objects.all().delete()
	for data in datalist:
		#if (data['kpp']) and (data['regno']) and (data['datenp']) and (data['datekf']):
		if (data['id']):
			print "\t", data['id'], data['name'], data['datekf'], data['datevv']
			org = models.Org(
				name		= data['name'],
				fullname	= data['fullname'],
				okopf		= models.Okopf.objects.get(pk=int(data['okopf'])),
				inn		= int(data['inn']),
				ogrn		= int(data['ogrn']),
				laddress	= data['laddr'],
				raddress	= data['raddr'],
				paysum		= 300000,
				comments	= data['comments'],
			)
			if (data['kpp']):
				kpp		= int(data['kpp'])
			if (data['regno']):
				sroregno	= int(data['regno'])
				sroregdate	= data['datenp']
			if (data['datekf']):
				paydate		= data['datekf']
			if (data['datevv']):
				paydatevv	= data['datevv'],
			org.save()
		else:
			print "Skiped: %s - %s,\tkpp: %s,\tregno: %s,\tdatenp: %s,\tdatekf: %s" % (data['id'], data['name'], data['kpp'], data['regno'], data['datenp'], data['datekf'])
	# phones
	# emails
	# license
	# stuff
