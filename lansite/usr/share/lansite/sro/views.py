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

def	__load_org(org_id, org=None):
	if (not org):
		org	= Org.objects.get(pk=org_id)
	return {
		'org':		org,
		'phone':	OrgPhone.objects.filter(org=org),
		'email':	OrgEmail.objects.filter(org=org),
		'stuff':	OrgStuff.objects.filter(org=org),
		'permit':	Permit.objects.filter(org=org),
		'event':	OrgEvent.objects.filter(org=org),
		'file':		OrgFile.objects.filter(org=org),
	}

def	org_view(request, org_id):
	return render_to_response('sro/org_view.html', __load_org(org_id))

def	org_edit_main(request, org_id = None):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgMainForm(request.POST, instance=org)
		if form.is_valid():
			form.save()
			#new_org = form.save(commit=False)
                        #new_org.id = org.id
                        #new_org.save()
			return HttpResponseRedirect('../../view/')
#		else:
#			return render_to_response('sro/org_edit_main.html', { 'form': form, 'org': org})
	else:
		form = OrgMainForm(instance=org)
		okopf = Okopf.objects.all()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_main.html', formdict)

def	org_edit_okved(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':	# add
		OrgOkved(org=org, okved=Okved.objects.get(pk=request.POST['okved'])).save()
	formdict = __load_org(org_id, org)
	formdict['okved'] = Okved.objects.all()
	return render_to_response('sro/org_edit_okved.html', formdict)

def	org_edit_okved_del(request, org_id, item_id):
	OrgOkved.objects.get(org=Org.objects.get(pk=org_id), okved=Okved.objects.get(pk=item_id)).delete()
	return HttpResponseRedirect('../../')

def	org_edit_phone(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgPhoneForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			sid = request.POST['country'] + request.POST['trunk'] + request.POST['phone']
			if request.POST['ext']:
				sid += request.POST['ext']
			new_item.id = int(sid)
			new_item.org = org
			new_item.save()
			form = OrgPhoneForm()
	else:
		form = OrgPhoneForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_phone.html', formdict)

def	org_edit_phone_del(request, org_id, item_id):
	OrgPhone.objects.get(pk=item_id).delete()
	return HttpResponseRedirect('../../')

def	org_edit_email(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgEmailForm(request.POST)
		if form.is_valid():
			orgemail = OrgEmail(org=org, URL=form.cleaned_data['email'])
			orgemail.save()
			form = OrgEmailForm()
	else:
		form = OrgEmailForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_email.html', formdict)

def	org_edit_email_del(request, org_id, item_id):
	OrgEmail.objects.get(pk=item_id).delete()
	return HttpResponseRedirect('../../')

def	org_edit_stuff(request, org_id = None):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgStuffForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = org
			new_item.save()
			form = OrgStuffForm()
	else:
		form = OrgStuffForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_stuff.html', formdict)

def	org_edit_stuff_del(request, org_id, item_id):
	OrgStuff.objects.get(pk=item_id).delete()
	return HttpResponseRedirect('../../')

def	org_view_permit(request, org_id, item_id):
	#org = Org.objects.get(pk=org_id)
	#return render_to_response('sro/org_view_permit.html', {'org': org})
	return HttpResponseRedirect('../../')

def	org_edit_permit(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = PermitForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = org
			new_item.save()
			form = PermitForm()
	else:
		form = PermitForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_permit.html', formdict)

def	org_edit_permit_del(request, org_id, item_id):
	Permit.objects.get(pk=item_id).delete()
	return HttpResponseRedirect('../../')

def	org_edit_event(request, org_id):
	return render_to_response('sro/dummy.html')

def	org_edit_event_del(request, org_id, item_id):
	return HttpResponseRedirect('../../')

def	org_edit_file(request, org_id):
	return render_to_response('sro/dummy.html')

def	org_edit_file_del(request, org_id, item_id):
	return HttpResponseRedirect('../../')

def	org_del(request, org_id):
	org = Org.objects.get(pk=org_id)
	return render_to_response('sro/dummy.html', {'org': org})

def	org_add(request):
	return render_to_response('sro/dummy.html', {'org': org})

def	person(request):
	return render_to_response('sro/dummy.html')

def	meeting(request):
	return render_to_response('sro/dummy.html')
