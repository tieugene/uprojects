# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.db import transaction
from django.core import serializers

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

@transaction.commit_manually
def	importxml(request):
	if (request.method == 'POST'):
		form = ImportForm(request.POST, request.FILES)
		#pprint.pprint(request.FILES.keys())
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
