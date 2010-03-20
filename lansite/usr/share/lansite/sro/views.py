# -*- coding: utf-8 -*-
'''
SRO views
'''
# 1. django
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.db import transaction
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode, smart_str
# 2. other python
from xml.sax import handler, make_parser
from datetime import datetime
import ftplib, netrc, tempfile
from trml2pdf import trml2pdf
import pprint
# 3. my
from models import *
from forms import *
from impex import *

def	__log_it(request, object, action, change_message=''):
	'''
	Log this activity
	'''
	LogEntry.objects.log_action(
		user_id         = request.user.id, 
		content_type_id = ContentType.objects.get_for_model(object).pk, 
		object_id       = object.pk, 
		object_repr     = object.asstr(), # Message you want to show in admin action list
		change_message  = u'UI: ' + change_message, # I used same
		action_flag     = action	# django.contrib.admin.models: ADDITION/CHANGE/DELETION
	)

def	pdf_render_to_response(template, context, filename=None):
	response = HttpResponse(mimetype='application/pdf')
	if not filename:
		filename = template+'.pdf'
	cd = []
	cd.append('filename=%s' % filename)
	response['Content-Disposition'] = '; '.join(cd)
	tpl = loader.get_template(template)
	tc = {'filename': filename}
	tc.update(context)
	response.write(trml2pdf.parseString(tpl.render(Context(tc)).encode('utf-8')))
	return response

def	index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('../login/?next=%s' % request.path)
	return render_to_response('sro/index.html', context_instance=RequestContext(request))

def	journal(request):
	return render_to_response('sro/journal.html', RequestContext(request, {'log': LogEntry.objects.all()}))

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

@login_required
def	org_list(request):
	if request.method == 'POST':
		if (request.POST['okato']):
			org_list = Org.objects.filter(okato__pk=request.POST['okato'])
		elif (request.POST['insurer']):
			org_list = Org.objects.filter(orginsurance__insurer__pk=request.POST['insurer'])
		else:
			org_list = Org.objects.all()
	else:
		org_list = Org.objects.all()
	org_list = org_list.order_by('name')
	return render_to_response('sro/org_list.html', RequestContext(request, {'org_list': org_list, 'form': OrgListForm()}))

def	org_publish_s(request):
	org_list = Org.objects.filter(public=True).order_by('name')
	return render_to_response('sro/org_publish_s.html', RequestContext(request, {'org_list': org_list, 'dt': datetime.now().strftime('%d.%m.%Y %H:%M:%S')}))

def	org_publish_p(request):
	org_list = Org.objects.filter(prjorg__publish=True).order_by('name')
	return render_to_response('sro/org_publish_p.html', RequestContext(request, {'org_list': org_list, 'dt': datetime.now().strftime('%d.%m.%Y %H:%M:%S')}))

def	__org_upload(request, html, ftppath):
	ftpname = 'ftp.moozs.ru'
	hosts = netrc.netrc('/mnt/shares/lansite/media/netrc').hosts
	if (not hosts.has_key(ftpname)):
		return render_to_response('sro/upload_msg.html', {'msg': "Check netrc"})
	f = tempfile.TemporaryFile()
	f.write(html)
	f.seek(0)
	login, acct, password = hosts[ftpname]
	ftp = ftplib.FTP(ftpname, login, password)
	ftp.storbinary('STOR %s' % ftppath, f)
	ftp.quit()
	f.close()
	return render_to_response('sro/upload_msg.html', RequestContext(request, {'msg': "Uploaded OK"}))

def	org_upload_s(request):
	org_list = Org.objects.filter(public=True).order_by('name')
	html = loader.get_template('sro/org_publish_s.html').render(Context({'org_list': org_list, 'dt': datetime.now().strftime('%d.%m.%Y %H:%M:%S')})).encode('windows-1251')
	return __org_upload(request, html, '/moozs.ru/docs/joom/images/members.htm')

def	org_upload_p(request):
	org_list = Org.objects.filter(prjorg__publish=True).order_by('name')
	t = loader.get_template('sro/org_publish_p.html')
	html = t.render(Context({'org_list': org_list, 'dt': datetime.now().strftime('%d.%m.%Y %H:%M:%S')})).encode('windows-1251')
	return __org_upload(request, html, 'mooasp.ru/docs/joom/images/stories/docs/members.htm')

def	org_table(request):
	org_list = Org.objects.all().order_by('name')
	return render_to_response('sro/org_table.html', RequestContext(request, {'org_list': org_list}))

def	org_mailto(request):
	s = ""
	sep = ""
	for i in OrgEmail.objects.all():
		s = s + sep + i.URL
		if not sep:
			sep = ", "
	return render_to_response('sro/org_mailto.html', RequestContext(request, {'mailto': s}))

def	org_del(request, org_id):
	org = Org.objects.get(pk=org_id)
	__log_it(request, org, DELETION)
	org.delete()
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
	return render_to_response('sro/org_view.html', RequestContext(request, __load_org(org_id)))

def	org_svid_pdf(request, org_id):
	org = Org.objects.get(pk=org_id)
	data = dict()
	data['org'] = org
	data['date'] = __strdate(org.sroregdate)
	data['bigdate'] = __strdate(org.sroregdate).upper()
	return pdf_render_to_response('sro/svid.rml', {'data': data}, filename=str(org.sroregno) + '.pdf')

def	org_extract(request, org_id):
	org = Org.objects.get(pk=org_id)
	#perm = Permit.objects.get(org=org, permittype=PermitType.objects.get(pk=1))
	ptype = PermitType.objects.get(pk=1)
	perms = Permit.objects.filter(org=org, permittype=ptype, permitown__date__lte=datetime.today())
	perm = perms.latest('permitown__date')
	changes = perms.filter(permitown__regno__lt=perm.permitown.regno)
	return render_to_response('sro/org_extract.html', RequestContext(request, { 'org': org, 'perm': perm, 'changes': changes, 'date': datetime.now() }))

def	org_add(request):
	org = Org()
	if request.method == 'POST':
		form = OrgMainForm(request.POST, instance=org)
		if form.is_valid():
			org = form.save()
			__log_it(request, org, ADDITION)
			return HttpResponseRedirect('../%d/' % org.id)
			#return HttpResponseRedirect(reverse('sro.org_view', args={'org_id': org.id}))
	else:
		form = OrgMainForm(instance=org)
		okopf =  Okopf.objects.all()
	return render_to_response('sro/org_edit_main.html', RequestContext(request, {'org': org, 'form': form}))

def	org_edit_main(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgMainForm(request.POST, instance=org)
		if form.is_valid():
			form.save()
			__log_it(request, org, CHANGE)
			#return HttpResponseRedirect(reverse('org_view', args=[org_id,]))
			return HttpResponseRedirect('../../')
	else:
		form = OrgMainForm(instance=org)
		okopf = Okopf.objects.all()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_main.html', RequestContext(request, formdict))

def	org_license_add(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = OrgLicenseForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = org
			new_item.save()
			#__log_it(request, org, "Org %s: license added" % org.name)
			return HttpResponseRedirect('../../')
	else:
		form = OrgLicenseForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_license.html', RequestContext(request, formdict))

def	org_license_edit(request, org_id):
	org = Org.objects.get(pk=org_id)
	formdict = __load_org(org_id, org)
	if request.method == 'POST':
		form = OrgLicenseForm(request.POST, instance=formdict['license'])
		if form.is_valid():
			form.save()
			#__log_it(request, org, "Org %s: license edited" % org.name)
			return HttpResponseRedirect('../../')
	else:
		form = OrgLicenseForm(instance=formdict['license'])
	formdict['form'] = form
	return render_to_response('sro/org_license.html', RequestContext(request, formdict))

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
	return render_to_response('sro/org_insurance.html', RequestContext(request, formdict))

def	org_insurance_edit(request, org_id):
	org = Org.objects.get(pk=org_id)
	formdict = __load_org(org_id, org)
	if request.method == 'POST':
		form = OrgInsuranceForm(request.POST, instance=formdict['insurance'])
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('../../')
	else:
		form = OrgInsuranceForm(instance=formdict['insurance'])
	formdict['form'] = form
	return render_to_response('sro/org_insurance.html', RequestContext(request, formdict))

def	org_insurance_del(request, org_id):
	OrgInsurance.objects.filter(org=Org.objects.get(pk=org_id))[0].delete()
	return HttpResponseRedirect('../../')

def	org_edit_okved(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':	# add
		OrgOkved(org=org, okved=Okved.objects.get(pk=request.POST['okved'])).save()
	formdict = __load_org(org_id, org)
	formdict['okved'] = Okved.objects.all()
	return render_to_response('sro/org_edit_okved.html', RequestContext(request, formdict))

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
	return render_to_response('sro/org_edit_phone.html', RequestContext(request, formdict))

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
	return render_to_response('sro/org_edit_email.html', RequestContext(request, formdict))

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
	return render_to_response('sro/org_edit_www.html', RequestContext(request, formdict))

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
		form = OrgStuffForm_Soft(request.GET)
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	formdict['form_person'] = OrgStuffAddPersonForm()
	formdict['form_role'] = OrgStuffAddRoleForm()
	return render_to_response('sro/org_edit_stuff.html', RequestContext(request, formdict))

def	org_edit_stuff_add_person(request, org_id):
	if request.method == 'POST':
		form = OrgStuffAddPersonForm(request.POST)
		if form.is_valid():
			item = form.save()
			#org = Org.objects.get(pk=org_id)
			#formdict = __load_org(org_id, org)
			#formdict['form'] = OrgStuffForm(person=person)
			#formdict['form_person'] = OrgStuffAddPersonForm()
			#formdict['form_role'] = OrgStuffAddRoleForm()
	return HttpResponseRedirect('../?person=%d' % item.id)

def	org_edit_stuff_add_role(request, org_id):
	if request.method == 'POST':
		form = OrgStuffAddRoleForm(request.POST)
		if form.is_valid():
			item = form.save()
	return HttpResponseRedirect('../?role=%d' % item.id)
	#return HttpResponseRedirect(reverse('org_edit_stuff', args=(int(org_id),)))

def	org_edit_stuff_del(request, org_id, item_id):
	OrgStuff.objects.get(pk=item_id).delete()
	return HttpResponseRedirect('../../')

def	org_edit_permit(request, org_id):
	org = Org.objects.get(pk=org_id)
	if request.method == 'POST':
		form = PermitForm(request.POST)
		if form.is_valid():
			permittype = form.cleaned_data['permittype']
			#new_item = form.save(commit=False)
			#new_item.org = org
			#new_item.save()
			return HttpResponseRedirect('%s/add/' % permittype.id)
	else:
		form = PermitForm()
	formdict = __load_org(org_id, org)
	formdict['form'] = form
	return render_to_response('sro/org_edit_permit.html', RequestContext(request, formdict))

@transaction.commit_manually
def	org_edit_permit_add(request, org_id, type_id):
	'''
	Own permition
	'''
	org = Org.objects.get(pk=org_id)
	permittype = PermitType.objects.get(pk=type_id)
	type_id = int(type_id)
	needform = (PermitOwnForm, PermitStatementForm, PermitAlienForm)[type_id - 1]
	if request.method == 'POST':
		form = needform(request.POST)
		if form.is_valid():
			try:
				permit = Permit(org=org, permittype=permittype)
				permit.save()
				if (type_id == 1):
					a = PermitOwn(
						permit=permit,
						regno=form.cleaned_data['regno'],
						date=form.cleaned_data['date'],
						meeting=form.cleaned_data['meeting']
					)
				elif (type_id == 2):
					a = PermitStatement(
						permit=permit,
						date=form.cleaned_data['date']
					)
				else:
					a = PermitAlien(
						permit=permit,
						sro=form.cleaned_data['sro'],
						regno=form.cleaned_data['regno'],
						date=form.cleaned_data['date'],
						protono=form.cleaned_data['protono'],
						protodate=form.cleaned_data['protodate']
					)
				a.save()
			except:
				transaction.rollback()
			else:
				transaction.commit()
			return HttpResponseRedirect('../../')
	else:
		form = needform()
	formdict = {'org': org, 'permittype': permittype, 'form': form}
	return render_to_response('sro/org_edit_permit_add.html', RequestContext(request, formdict))

def	org_edit_permit_del(request, org_id, item_id):
	Permit.objects.get(pk=item_id).delete()
	return HttpResponseRedirect('../../')

def	org_edit_event(request, org_id):
	return render_to_response('sro/dummy.html')

def	org_edit_event_del(request, org_id, item_id):
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
	jcount = 0
	for ps in PermitStage.objects.filter(permit=perm):
		myjobs = dict()
		joblist = PermitStageJob.objects.filter(permitstage=ps)
		jc = joblist.count()
		if jc == 0:
			jc = 1
		jcount += jc
		for j in joblist:
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
	return render_to_response('sro/permit_list.html', RequestContext(request, { 'permit': perm, 'stages': stages, 'jcount': jcount, 'form': PermitListForm() }))

def	permit_edit(request, perm_id):
	permit = Permit.objects.get(pk=perm_id)
	type_id = permit.permittype.id
	if (type_id == 1):
		perm = permit.permitown
		needform = PermitOwnForm
	elif (type_id == 2):
		perm = permit.permitstatement
		needform = PermitStatementForm
	else:
		perm = permit.permitalien
		needform = PermitAlienForm
	if request.method == 'POST':
		form = needform(request.POST, instance=perm)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('../')
	else:
		form = needform(instance=perm)
	return render_to_response('sro/permit_edit.html', RequestContext(request, { 'form': form, 'permit': perm }))

@transaction.commit_manually
def	permit_edit_stage(request, perm_id, stage_id):
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
		return render_to_response('sro/permit_edit_stage.html', RequestContext(request, { 'permit': perm, 'stage': stage, 'sflag': sflag, 'jobs': jobs }))

def	__strdate(d):
	__mon = (u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря')
	return u'«%02d» %s %d года' % (d.day, __mon[d.month - 1], d.year)

def	__load_permit(perm_id):
	perm = Permit.objects.get(pk=perm_id)
	data = dict()
	data['perm']		= perm
	data['no']		= u'%d-%02d' % (perm.org.sroregno, perm.permitown.regno)
	data['date']		= __strdate(perm.permitown.date)
	data['protodate']	= __strdate(perm.permitown.meeting.date)
	jcount = 0
	for stage in PermitStage.objects.filter(permit=perm):
		count = PermitStageJob.objects.filter(permitstage=stage).count()
		if (count == 0):
			count = 1
		jcount = jcount + count
	data['jcount'] = jcount
	return data

def	permit_html(request, perm_id):
	return render_to_response('sro/permit_html.html', RequestContext(request, { 'data': __load_permit(perm_id) }))

def	permit_pdf(request, perm_id):
	data = __load_permit(perm_id)
	data['user'] = request.user.username
	return pdf_render_to_response('sro/permit.rml', {'data': data}, filename=data['no'] + '.pdf')

def	org_prj_pdf(request, org_id):
	org = Org.objects.get(pk=org_id)
	prjorg = org.prjorg
	data = dict()
	data['prjorg']		= prjorg
	data['date']		= __strdate(prjorg.permdate)
	data['protodate']	= __strdate(prjorg.protocol.date)
	data['user'] = request.user.username
	return pdf_render_to_response('sro/prj.rml', {'data': data}, filename=data['prjorg'].permno + '.pdf')

def	permit_dup(request, perm_id):
	if request.method == 'POST':
		form = PermitListForm(request.POST)
		if form.is_valid():
			permittype = form.cleaned_data['permittype']
			if (permittype):
				return HttpResponseRedirect('%d/' % permittype.id)
	return HttpResponseRedirect('../')

#@transaction.commit_manually
def	permit_dup_edit(request, perm_id, type_id):
	perm = Permit.objects.get(pk=perm_id)
	permittype = PermitType.objects.get(pk=type_id)
	type_id = int(type_id)
	needform = (PermitOwnForm, PermitStatementForm, PermitAlienForm)[type_id - 1]
	if request.method == 'POST':
		form = needform(request.POST)
		if form.is_valid():
			#try:
			if (True):
				# 1. main object
				permit = Permit(org=perm.org, permittype=permittype)
				permit.save()
				# 2. subobject
				if (type_id == 1):
					a = PermitOwn(
						permit=permit,
						regno=form.cleaned_data['regno'],
						date=form.cleaned_data['date'],
						meeting=form.cleaned_data['meeting']
					)
				elif (type_id == 2):
					a = PermitStatement(
						permit=permit,
						date=form.cleaned_data['date']
					)
				else:
					a = PermitAlien(
						permit=permit,
						sro=form.cleaned_data['sro'],
						regno=form.cleaned_data['regno'],
						date=form.cleaned_data['date'],
						protono=form.cleaned_data['protono'],
						protodate=form.cleaned_data['protodate']
					)
				a.save()
				# 3. copy jobs
				for ps in perm.permitstage_set.all():
					permitstage = PermitStage(permit=permit, stage=ps.stage)
					permitstage.save()
					for psj in ps.permitstagejob_set.all():
						PermitStageJob(permitstage=permitstage, job=psj.job).save()
			#except:
			#	transaction.rollback()
			#	print "except"
			#	return HttpResponseRedirect('../../')
			#else:
			#	transaction.commit()
			#	print 'commit'
				return HttpResponseRedirect('../../../%d' % permit.id)
	else:
		form = needform()
	formdict = {'org': perm.org, 'permittype': permittype, 'form': form}
	return render_to_response('sro/org_edit_permit_add.html', RequestContext(request, formdict))

def	permit_cmp(request, perm_id):
	pass

def	person_list(request):
	person_list = Person.objects.all().order_by('lastname')
	return render_to_response('sro/person_list.html', RequestContext(request, {'person_list': person_list}))

def	person_del(request, person_id):
	Person.objects.get(pk=person_id).delete()
	return HttpResponseRedirect('../../')

def	person_view(request, person_id):
	person	= Person.objects.get(pk=person_id)
	skill	= PersonSkill.objects.filter(person=person)
	return render_to_response('sro/person_view.html', RequestContext(request, { 'person': person, 'person_skill': skill }))

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
	return render_to_response('sro/person_main.html', RequestContext(request, { 'person': person, 'person_skill': skill, 'form': form } ))

def	person_skill(request, person_id):
	person = Person.objects.get(pk=person_id)
	if request.method == 'POST':
		form = PersonSkillForm(request.POST)
		if form.is_valid():
		#if (True):
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
	return render_to_response('sro/person_skill.html', RequestContext(request, formdict))

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