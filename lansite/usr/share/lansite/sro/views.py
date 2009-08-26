# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.db import transaction
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
from xml.sax import handler, make_parser
from datetime import datetime

import pprint

from models import *
from forms import *
from impex import *

@login_required
def	index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/?next=%s' % request.path)
	#print request.user.username
	return render_to_response('sro/index.html', context_instance=RequestContext(request))

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

def	org_list(request):
	org_list = Org.objects.all().order_by('id')
	return render_to_response('sro/org_list.html', {'org_list': org_list})

def	org_publish(request):
	org_list = Org.objects.all().order_by('id')
	return render_to_response('sro/org_publish.html', {'org_list': org_list})

def	org_del(request, org_id):
	Org.objects.get(pk=org_id).delete()
	return HttpResponseRedirect('../../')

def	__load_org(org_id, org=None):
	if (not org):
		org	= Org.objects.get(pk=org_id)
	retvalue = {
		'org':		org,
		'phone':	OrgPhone.objects.filter(org=org),
		'email':	OrgEmail.objects.filter(org=org),
		'www':		OrgWWW.objects.filter(org=org),
		'stuff':	OrgStuff.objects.filter(org=org),
		'permit':	Permit.objects.filter(org=org),
		'event':	OrgEvent.objects.filter(org=org),
		'file':		OrgFile.objects.filter(org=org),
	}
	tmp = OrgLicense.objects.filter(org=org)
	if tmp:
		retvalue['license'] = tmp[0]
	else:
		retvalue['license'] = None
	tmp = OrgInsurance.objects.filter(org=org)
	if tmp:
		retvalue['insurance'] = tmp[0]
	else:
		retvalue['insurance'] = None
	return retvalue

def	org_view(request, org_id):
	return render_to_response('sro/org_view.html', __load_org(org_id))

def	org_add(request):
	org = Org()
	if request.method == 'POST':
		form = OrgMainForm(request.POST, instance=org)
		if form.is_valid():
			org = form.save()
			return HttpResponseRedirect('../%d/' % org.id)
	else:
		form = OrgMainForm(instance=org)
		okopf =  Okopf.objects.all()
	return render_to_response('sro/org_edit_main.html', {'org': org, 'form': form})

def	org_edit_main(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgMainForm(request.POST, instance=org)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('../../')
	else:
		form = OrgMainForm(instance=org)
		okopf = Okopf.objects.all()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_main.html', formdict)

def	org_license_add(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgLicenseForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = org
			new_item.save()
			return HttpResponseRedirect('../../')
	else:
		form = OrgLicenseForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_license.html', formdict)

def	org_license_del(request, org_id):
	OrgLicense.objects.filter(org=Org.objects.get(pk=org_id))[0].delete()
	return HttpResponseRedirect('../../')

def	org_insurance_add(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgInsuranceForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = org
			new_item.save()
			return HttpResponseRedirect('../../')
	else:
		form = OrgInsuranceForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_insurance.html', formdict)

def	org_insurance_del(request, org_id):
	OrgInsurance.objects.filter(org=Org.objects.get(pk=org_id))[0].delete()
	return HttpResponseRedirect('../../')

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

def	org_edit_www(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgWWWForm(request.POST)
		if form.is_valid():
			orgwww = OrgWWW(org=org, URL=form.cleaned_data['www'])
			orgwww.save()
			form = OrgWWWForm()
	else:
		form = OrgWWWForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_www.html', formdict)

def	org_edit_www_del(request, org_id, item_id):
	OrgWWW.objects.get(pk=item_id).delete()
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
	formdict['form_person'] = OrgStuffAddPersonForm()
	formdict['form_role'] = OrgStuffAddRoleForm()
	return render_to_response('sro/org_edit_stuff.html', formdict)

def	org_edit_stuff_add_person(request, org_id):
	if request.method == 'POST':
		form = OrgStuffAddPersonForm(request.POST)
		if form.is_valid():
			form.save()
	return HttpResponseRedirect('../')

def	org_edit_stuff_add_role(request, org_id):
	if request.method == 'POST':
		form = OrgStuffAddRoleForm(request.POST)
		if form.is_valid():
			form.save()
	return HttpResponseRedirect('../')

def	org_edit_stuff_del(request, org_id, item_id):
	OrgStuff.objects.get(pk=item_id).delete()
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

@transaction.commit_manually
def	permit_list(request, perm_id):
	perm = Permit.objects.get(pk=perm_id)
	if request.method == 'POST':	# no valid - just save
		try:
		#if (True):
			# 1. delete all
			ps = PermitStage.objects.filter(permit=perm)
			if (ps):
				ps.delete()
			# 2. add all Stages
			for sid in request.POST.getlist('set'):		# [u'<id>', ...]
				stage = Stage.objects.get(pk=sid)
				ps = PermitStage(permit=perm, stage=stage)
				ps.save()
			# 2.1 add all jobs
				for j in Job.objects.filter(stage=stage):
					PermitStageJob(permitstage=ps, job=j).save()
		except:
			transaction.rollback()
		else:
			transaction.commit()
		#return HttpResponseRedirect('.')	# FIXME:
	#else:	# GET
	mystages = {}
	for ps in PermitStage.objects.filter(permit=perm):
		myjobs = dict()
		for j in PermitStageJob.objects.filter(permitstage=ps):
			myjobs[j.job.id] = True
		mystages[ps.stage.id] = myjobs
	stages = []		# [(stage, flag, jobs),]
	for s in Stage.objects.all():
		sid = int(s.id)
		sflag = sid in mystages
		jobs = list()	# [(job, flag),]
		for j in Job.objects.filter(stage=s):
			if (sflag):
				jobs.append((j, int(j.id) in mystages[sid]))
			else:
				jobs.append((j, False))
		stages.append((s, sflag, jobs))
	#pprint.pprint(stages)
	return render_to_response('sro/permit_list.html', { 'permit': perm, 'stages': stages })

@transaction.commit_manually
def	permit_edit(request, perm_id, stage_id):
	perm = Permit.objects.get(pk=perm_id)
	if request.method == 'POST':	# no valid - just save
		stage = Stage.objects.get(pk=stage_id)
		# 1. delete all
		try:
		#if (True):
			ps = PermitStage.objects.filter(permit=perm, stage=stage)
			if (ps):
				ps.delete()
			if (request.POST.get('g')):			# u'on' | None
				# 2. create new PermitStage
				ps = PermitStage(permit=perm, stage=stage)
				ps.save()
				for i in request.POST.getlist('id'):	# [u'<id>', ...]
					# 2.1 add jobs
					PermitStageJob(permitstage=ps, job=Job.objects.get(pk=i)).save()
		except:
			transaction.rollback()
		else:
			transaction.commit()
		return HttpResponseRedirect('../../')	# FIXME:
	else:	# GET
		stage = Stage.objects.get(id=stage_id)
		mystages = PermitStage.objects.filter(permit=perm, stage=stage_id)
		myjobs = {}	# jobs of current stage
		if (mystages):
			sflag = True
			for j in PermitStageJob.objects.filter(permitstage=mystages[0]):
				myjobs[j.job.id] = True
		else:
			sflag = False
		jobs = []
		for j in Job.objects.filter(stage=stage):
			jobs.append((j, j.id in myjobs))
		return render_to_response('sro/permit_edit.html', { 'permit': perm, 'stage': stage, 'sflag': sflag, 'jobs': jobs })

def	person_list(request):
	person_list = Person.objects.all().order_by('lastname')
	return render_to_response('sro/person_list.html', {'person_list': person_list})

def	person_del(request, person_id):
	Person.objects.get(pk=person_id).delete()
	return HttpResponseRedirect('../../')

def	person_view(request, person_id):
	person	= Person.objects.get(pk=person_id)
	skill	= PersonSkill.objects.filter(person=person)
	return render_to_response('sro/person_view.html', { 'person': person, 'person_skill': skill })

def	person_main(request, person_id):
	person	= Person.objects.get(pk=person_id)
	skill	= PersonSkill.objects.filter(person=person)
	if request.method == 'POST':
		form = PersonMainForm(request.POST, instance=person)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('../')
	else:
		form = PersonMainForm(instance=person)
	return render_to_response('sro/person_main.html', { 'person': person, 'person_skill': skill, 'form': form } )

def	person_skill(request, person_id):
	person = Person.objects.get(pk=person_id)
	if request.method == 'POST':
		#print "adding:", request.POST
		form = PersonSkillForm(request.POST)
		if form.is_valid():
		#if (True):
			#print "form valid"
			#pprint.pprint(form)
			new_item = form.save(commit=False)
			new_item.person = person
			new_item.save()
			form = PersonSkillForm()
	else:
		form = PersonSkillForm()
	formdict = dict()
	formdict['person']		= person
	formdict['person_skill']	= PersonSkill.objects.filter(person=person)
	formdict['speciality']		= Speciality.objects.all()
	formdict['skill']		= Skill.objects.all()
	formdict['form']		= form
	formdict['form_speciality']	= PersonSkillAddSpecialityForm()
	formdict['form_skill']		= PersonSkillAddSkillForm()
	return render_to_response('sro/person_skill.html', formdict)

def	person_skill_add_speciality(request, person_id):
	if request.method == 'POST':
		form = PersonSkillAddSpecialityForm(request.POST)
		if form.is_valid():
			form.save()
	return HttpResponseRedirect('../')

def	person_skill_add_skill(request, person_id):
	if request.method == 'POST':
		form = PersonSkillAddSkillForm(request.POST)
		if form.is_valid():
			form.save()
	return HttpResponseRedirect('../')

def	person_skill_del(request, person_id, item_id):
	PersonSkill.objects.get(pk=item_id).delete()
	return HttpResponseRedirect('../../')

def	meeting(request):
	return render_to_response('sro/dummy.html')
