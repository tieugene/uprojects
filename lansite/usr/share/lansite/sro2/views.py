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

def	__log_it(request, object, action, change_message=''):
	'''
	Log this activity
	'''
	LogEntry.objects.log_action(
		user_id         = request.user.id,
		content_type_id = ContentType.objects.get_for_model(object).pk,
		object_id       = object.pk, 
		object_repr     = object.asstr(), # Message you want to show in admin action list
		change_message  = u'SRO2.UI: ' + change_message, # I used same
		action_flag     = action	# django.contrib.admin.models: ADDITION/CHANGE/DELETION
	)

def	__pdf_render_to_response(template, context, filename=None):
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

def	__strdate(d):
	__mon = (u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря')
	return u'«%02d» %s %d года' % (d.day, __mon[d.month - 1], d.year)

def	__load_permit(perm_id):
	stagelist = StageList.objects.get(pk=perm_id)
	jcount = 0
	for stage in PermitStage.objects.filter(stagelist=stagelist):
		count = PermitStageJob.objects.filter(permitstage=stage).count()
		if (count == 0):
			count = 1
		jcount = jcount + count
	return {'stagelist': stagelist, 'date': __strdate(stagelist.permit.date), 'protodate': __strdate(stagelist.permit.protocol.date), 'jcount': jcount}

def	index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('../login/?next=%s' % request.path)
		#return HttpResponseRedirect(reverse('lansite.login') + '?next=%s' % request.path)
		#return HttpResponseRedirect(reverse('lansite.login') + '?next=%s' % request.path)
	return render_to_response('sro2/index.html', context_instance=RequestContext(request, {'sro_list': Sro.objects.filter(own=True).order_by('name')}))

@login_required
def	journal(request):
	return render_to_response('sro2/journal.html', RequestContext(request, {'log': LogEntry.objects.all()}))

@login_required
def	index_sro(request, sro_id):
	return render_to_response('sro2/index_sro.html', context_instance=RequestContext(request, {'sro': Sro.objects.get(pk=sro_id)}))

@login_required
def	sro_list(request, sro_id):
	sro = Sro.objects.get(pk=sro_id)
	orgsro_list = sro.orgsro_set.all().order_by('org__name')
	if request.method == 'POST':
		if (request.POST['okato']):
			orgsro_list = orgsro_list.filter(org__okato__pk=request.POST['okato'])
		elif (request.POST['insurer']):
			orgsro_list = orgsro_list.filter(orginsurance__insurer__pk=request.POST['insurer'])
	return render_to_response('sro2/sro_orglist.html', RequestContext(request, {'sro': sro, 'orgsro_list': orgsro_list, 'form': OrgListForm()}))

@login_required
def	sro_publish(request, sro_id):
	sro = Sro.objects.get(pk=sro_id)
	orgsro_list = sro.orgsro_set.filter(publish=True).order_by('org__name')
	return render_to_response('sro2/sro_publish.html', RequestContext(request, {'sro': sro, 'orgsro_list': orgsro_list, 'dt': datetime.now().strftime('%d.%m.%Y %H:%M:%S')}))

@login_required
def	sro_upload(request, sro_id):
	'''FIXME'''
	sro = Sro.objects.get(pk=sro_id)
	orgsro_list = sro.orgsro_set.filter(publish=True).order_by('org__name')
	ftpname = sro.sroown.ftp
	hosts = netrc.netrc('/mnt/shares/lansite/media/netrc').hosts
	if (not hosts.has_key(ftpname)):
		return render_to_response('sro2/upload_msg.html', {'msg': "Check netrc"})
	t = loader.get_template('sro2/sro_publish.html')
	html = t.render(Context({'orgsro_list': orgsro_list, 'dt': datetime.now().strftime('%d.%m.%Y %H:%M:%S')})).encode('windows-1251')
	f = tempfile.TemporaryFile()
	f.write(html)
	f.seek(0)
	login, acct, password = hosts[ftpname]
	ftp = ftplib.FTP(ftpname, login, password)
	ftp.storbinary('STOR %s/members.htm' % sro.sroown.path, f)
	ftp.quit()
	f.close()
	return render_to_response('sro2/upload_msg.html', RequestContext(request, {'msg': "Uploaded OK"}))

@login_required
def	sro_table(request, sro_id):
	sro = Sro.objects.get(pk=sro_id)
	orgsro_list = sro.orgsro_set.all().order_by('org__name')
	return render_to_response('sro2/sro_table.html', RequestContext(request, {'orgsro_list': orgsro_list}))

@login_required
def	sro_mailto(request, sro_id):
	'''FIXME'''
	s = ""
	sep = ""
	for i in OrgEmail.objects.all():
		s = s + sep + i.URL
		if not sep:
			sep = ", "
	return render_to_response('sro2/sro_mailto.html', RequestContext(request, {'mailto': s}))

@login_required
def	sro_org_add(request, sro_id):
	sro = Sro.objects.get(pk=sro_id)
	org = Org()
	if request.method == 'POST':
		form = OrgAddForm(request.POST, instance=org)
		if form.is_valid():
			org = form.save()
			__log_it(request, org, ADDITION)
			orgsro = OrgSro(org=org, sro=sro)
			orgsro.save()
			__log_it(request, orgsro, ADDITION)
			return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
	else:
		form = OrgAddForm(instance=org)
		okopf =  Okopf.objects.all()
	return render_to_response('sro2/sro_org_add.html', RequestContext(request, {'sro': sro, 'org': org, 'form': form}))

@login_required
def	orgsro_del(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	sro_id = orgsro.sro.id
	org = orgsro.org
	__log_it(request, orgsro, DELETION)
	orgsro.delete()
	if (org.orgsro_set.all().count() == 0):
		__log_it(request, org, DELETION)
		org.delete()
	return HttpResponseRedirect(reverse('sro2.views.sro_list', kwargs={'sro_id': sro_id}))

@login_required
def	orgsro_view(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	return render_to_response('sro2/orgsro_view.html', RequestContext(request, {'orgsro': orgsro}))


@login_required
def	orgsro_certificate(request, orgsro_id):
	'''FIXME'''
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	data = dict()
	data['orgsro'] = orgsro
	data['date'] = __strdate(orgsro.regdate)
	data['bigdate'] = __strdate(orgsro.regdate).upper()
	return __pdf_render_to_response('sro2/certificate.rml', {'data': data}, filename=str(orgsro.regno) + '.pdf')

@login_required
def	orgsro_extract(request, orgsro_id):
	'''FIXME'''
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	#perm = Permit.objects.get(org=org, type=StageListType.objects.get(pk=1))
	ptype = StageListType.objects.get(pk=2)
	stagelists = StageList.objects.filter(orgsro=orgsro, type=ptype, permit__date__lte=datetime.today())
	permit = stagelists.latest('permit__date')
	changes = stagelists.filter(permit__no__lt=permit.permit.no)
	return render_to_response('sro2/orgsro_extract.html', RequestContext(request, { 'orgsro': orgsro, 'permit': permit, 'changes': changes, 'date': datetime.now() }))

@login_required
def	orgsro_org_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	org = orgsro.org
	if request.method == 'POST':
		form = OrgEditForm(request.POST, instance=org)
		if form.is_valid():
			org = form.save()
			__log_it(request, org, CHANGE)
			return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
	else:
		form = OrgEditForm(instance=org)
		okopf = Okopf.objects.all()
	return render_to_response('sro2/orgsro_org.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_main_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgSroForm(request.POST, instance=orgsro)
		if form.is_valid():
			orgsro = form.save()
			__log_it(request, orgsro, CHANGE)
			return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
	else:
		form = OrgSroForm(instance=orgsro)
	return render_to_response('sro2/orgsro_main.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_license_add(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgLicenseForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.orgsro = orgsro
			new_item.save()
			__log_it(request, new_item, ADDITION)
			return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
	else:
		form = OrgLicenseForm()
	return render_to_response('sro2/orgsro_license.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_license_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = orgsro.orglicense
	if request.method == 'POST':
		form = OrgLicenseForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			__log_it(request, item, CHANGE)
			return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
	else:
		form = OrgLicenseForm(instance=item)
	return render_to_response('sro2/orgsro_license.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_license_del(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = orgsro.orglicense
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))

@login_required
def	orgsro_insurance_add(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgInsuranceForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.orgsro = orgsro
			new_item.save()
			__log_it(request, new_item, ADDITION)
			return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
	else:
		form = OrgInsuranceForm()
	return render_to_response('sro2/orgsro_insurance.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_insurance_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = orgsro.orginsurance
	if request.method == 'POST':
		form = OrgInsuranceForm(request.POST, instance=item)
		if form.is_valid():
			item = form.save()
			__log_it(request, item, CHANGE)
			return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))
	else:
		form = OrgInsuranceForm(instance=item)
	return render_to_response('sro2/orgsro_insurance.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_insurance_del(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = orgsro.orginsurance
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.orgsro_view', kwargs={'orgsro_id': orgsro.id}))

@login_required
def	orgsro_okved_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':	# add
		item = OrgOkved(org=orgsro.org, okved=Okved.objects.get(pk=request.POST['okved']))
		item.save()
		__log_it(request, item, CHANGE)
	return render_to_response('sro2/orgsro_okved.html', RequestContext(request, {'orgsro': orgsro, 'okved': Okved.objects.all()}))

@login_required
def	orgsro_okved_del(request, orgsro_id, item_id):
	''' FIXME: '''
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = OrgOkved.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.orgsro_okved_edit', kwargs={'orgsro_id': orgsro.id}))

@login_required
def	orgsro_phone_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgPhoneForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = orgsro.org
			new_item.save()
			__log_it(request, new_item, ADDITION)
			form = OrgPhoneForm()
	else:
		form = OrgPhoneForm()
	return render_to_response('sro2/orgsro_phone.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_phone_del(request, orgsro_id, item_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = OrgPhone.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.orgsro_phone_edit', kwargs={'orgsro_id': orgsro.id}))

@login_required
def	orgsro_email_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgEmailForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = orgsro.org
			new_item.save()
			__log_it(request, new_item, ADDITION)
			form = OrgEmailForm()
	else:
		form = OrgEmailForm()
	return render_to_response('sro2/orgsro_email.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_email_del(request, orgsro_id, item_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = OrgEmail.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.orgsro_email_edit', kwargs={'orgsro_id': orgsro.id}))

@login_required
def	orgsro_www_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgWWWForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = orgsro.org
			new_item.save()
			__log_it(request, new_item, ADDITION)
			form = OrgWWWForm()
	else:
		form = OrgWWWForm()
	return render_to_response('sro2/orgsro_www.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@login_required
def	orgsro_www_del(request, orgsro_id, item_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = OrgWWW.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.orgsro_www_edit', kwargs={'orgsro_id': orgsro.id}))

@login_required
def	orgsro_stuff_edit(request, orgsro_id = None):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgStuffForm(request.POST)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.org = orgsro.org
			new_item.save()
			__log_it(request, new_item, CHANGE)
			form = OrgStuffForm()
	else:
		form = OrgStuffForm_Soft(request.GET)
	return render_to_response('sro2/orgsro_stuff.html', RequestContext(request,  {'orgsro': orgsro, 'form': form, 'form_person': OrgStuffAddPersonForm(), 'form_role': OrgStuffAddRoleForm()}))

@login_required
def	orgsro_stuff_add_person(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgStuffAddPersonForm(request.POST)
		if form.is_valid():
			item = form.save()
			__log_it(request, item, ADDITION)
	return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={'orgsro_id': orgsro.id}) + '?person=%d' % item.id)

@login_required
def	orgsro_stuff_add_role(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = OrgStuffAddRoleForm(request.POST)
		if form.is_valid():
			item = form.save()
			__log_it(request, item, ADDITION)
	return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={'orgsro_id': orgsro.id}) + '?role=%d' % item.id)

@login_required
def	orgsro_stuff_del(request, orgsro_id, item_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = OrgStuff.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.orgsro_stuff_edit', kwargs={'orgsro_id': orgsro.id}))

@login_required
def	orgsro_stagelist_edit(request, orgsro_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	if request.method == 'POST':
		form = StageListForm(request.POST)
		if form.is_valid():
			type = form.cleaned_data['type']
			return HttpResponseRedirect(reverse('sro2.views.orgsro_stagelist_add', kwargs={'orgsro_id': orgsro.id, 'type_id': type.id}))
	else:
		form = StageListForm()
	return render_to_response('sro2/orgsro_stagelist.html', RequestContext(request, {'orgsro': orgsro, 'form': form}))

@transaction.commit_manually
def	orgsro_stagelist_add(request, orgsro_id, type_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	type = StageListType.objects.get(pk=type_id)
	type_id = int(type_id)
	needform = (StatementForm, PermitForm)[type_id - 1]
	if request.method == 'POST':
		form = needform(request.POST)
		if form.is_valid():
			try:
				stagelist = StageList(orgsro=orgsro, type=type)
				stagelist.save()
				if (type_id == 1):
					item = Statement(
						stagelist=stagelist,
						date=form.cleaned_data['date']
					)
				else:	# (type_id == 2):
					item = Permit(
						stagelist=stagelist,
						no=form.cleaned_data['no'],
						date=form.cleaned_data['date'],
						protocol=form.cleaned_data['protocol']
					)
				item.save()
			except:
				transaction.rollback()
			else:
				transaction.commit()
			if (item.id):
				__log_it(request, stagelist, ADDITION)
				__log_it(request, item, ADDITION)
				transaction.commit()
			return HttpResponseRedirect(reverse('sro2.views.orgsro_stagelist_edit', kwargs={'orgsro_id': orgsro.id}))
	else:
		form = needform()
	return render_to_response('sro2/orgsro_stagelist_add.html', RequestContext(request, {'orgsro': orgsro, 'type': type, 'form': form}))

@login_required
def	orgsro_stagelist_del(request, orgsro_id, item_id):
	orgsro = OrgSro.objects.get(pk=orgsro_id)
	item = StageList.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.orgsro_stagelist_edit', kwargs={'orgsro_id': orgsro.id}))

@login_required
def	orgsro_event_edit(request, orgsro_id):
	return render_to_response('sro2/dummy.html')

@login_required
def	orgsro_event_del(request, orgsro_id, item_id):
	return HttpResponseRedirect('sro2/dummy.html')

@login_required
def	person_list(request, sro_id):
	person_list = Person.objects.all().order_by('lastname')
	return render_to_response('sro2/person_list.html', RequestContext(request, { 'sro': Sro.objects.get(pk=sro_id), 'person_list': person_list}))

@login_required
def	person_view(request, sro_id, person_id):
	person	= Person.objects.get(pk=person_id)
	skill	= PersonSkill.objects.filter(person=person)
	return render_to_response('sro2/person_view.html', RequestContext(request, { 'sro': Sro.objects.get(pk=sro_id), 'person': person, 'person_skill': skill }))

@login_required
def	person_del(request, sro_id, person_id):
	item = Person.objects.get(pk=person_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.person_list', kwargs={'sro_id': sro_id}))

@login_required
def	person_main(request, sro_id, person_id):
	person	= Person.objects.get(pk=person_id)
	skill	= PersonSkill.objects.filter(person=person)
	if request.method == 'POST':
		form = PersonMainForm(request.POST, instance=person)
		if form.is_valid():
			item = form.save()
			__log_it(request, item, ADDITION)
			return HttpResponseRedirect(reverse('sro2.views.person_list', kwargs={'sro_id': sro_id}))
	else:
		form = PersonMainForm(instance=person)
	return render_to_response('sro2/person_main.html', RequestContext(request, { 'sro': Sro.objects.get(pk=sro_id), 'person': person, 'person_skill': skill, 'form': form } ))

@login_required
def	person_skill(request, sro_id, person_id):
	person = Person.objects.get(pk=person_id)
	if request.method == 'POST':
		form = PersonSkillForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.person = person
			item.save()
			__log_it(request, item, ADDITION)
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
	formdict['sro']			= Sro.objects.get(pk=sro_id)
	return render_to_response('sro2/person_skill.html', RequestContext(request, formdict))

@login_required
def	person_skill_add_speciality(request, sro_id, person_id):
	if request.method == 'POST':
		form = PersonSkillAddSpecialityForm(request.POST)
		if form.is_valid():
			item = form.save()
			__log_it(request, item, ADDITION)
	return HttpResponseRedirect(reverse('sro2.views.person_skill', kwargs={ 'sro_id': sro_id, 'person_id': person_id }))

@login_required
def	person_skill_add_skill(request, sro_id, person_id):
	if request.method == 'POST':
		form = PersonSkillAddSkillForm(request.POST)
		if form.is_valid():
			item = form.save()
			__log_it(request, item, ADDITION)
	return HttpResponseRedirect(reverse('sro2.views.person_skill', kwargs={ 'sro_id': sro_id, 'person_id': person_id }))

@login_required
def	person_skill_del(request, sro_id, person_id, item_id):
	item = PersonSkill.objects.get(pk=item_id)
	__log_it(request, item, DELETION)
	item.delete()
	return HttpResponseRedirect(reverse('sro2.views.person_skill', kwargs={ 'sro_id': sro_id, 'person_id': person_id }))

@transaction.commit_manually
def	stagelist_list(request, perm_id):
	stagelist = StageList.objects.get(pk=perm_id)
	if request.method == 'POST':	# no valid - just save
		result = False
		try:
		#if (True):
			# 1. delete all
			ps = PermitStage.objects.filter(stagelist=stagelist)
			if (ps):
				ps.delete()
			# 2. add all Stages
			for sid in request.POST.getlist('set'):		# [u'<id>', ...]
				stage = Stage.objects.get(pk=sid)
				ps = PermitStage(stagelist=stagelist, stage=stage)
				ps.save()
			# 2.1 add all jobs
				for j in Job.objects.filter(stage=stage):
					PermitStageJob(permitstage=ps, job=j).save()
		except:
			transaction.rollback()
		else:
			transaction.commit()
			result = True
		if (result):
			__log_it(request, stagelist, CHANGE, u'оптом')
			transaction.commit()
		#return HttpResponseRedirect('.')	# FIXME:
	#else:	# GET
	mystages = {}
	jcount = 0
	for ps in PermitStage.objects.filter(stagelist=stagelist):
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
	for s in Stage.objects.filter(srotype=stagelist.orgsro.sro.type):
		sid = int(s.id)
		sflag = sid in mystages
		jobs = list()	# [(job, flag),]
		for j in Job.objects.filter(stage=s):
			if (sflag):
				jobs.append((j, int(j.id) in mystages[sid]))
			else:
				jobs.append((j, False))
		stages.append((s, sflag, jobs))
	return render_to_response('sro2/stagelist_list.html', RequestContext(request, { 'stagelist': stagelist, 'stages': stages, 'jcount': jcount, 'form': StageListListForm() }))

@login_required
def	stagelist_edit(request, perm_id):
	stagelist = StageList.objects.get(pk=perm_id)
	type_id = stagelist.type.id
	if (type_id == 1):
		perm = stagelist.statement
		needform = StatementForm
	else:	# type_id == 2
		perm = stagelist.permit
		needform = PermitForm
	if request.method == 'POST':
		form = needform(request.POST, instance=perm)
		if form.is_valid():
			item = form.save()
			__log_it(request, stagelist, CHANGE)
			return HttpResponseRedirect(reverse('sro2.views.stagelist_list', kwargs={ 'perm_id': perm_id }))
	else:
		form = needform(instance=perm)
	return render_to_response('sro2/stagelist_edit.html', RequestContext(request, { 'form': form, 'stagelist': perm }))

@transaction.commit_manually
def	stagelist_edit_stage(request, perm_id, stage_id):
	stagelist = StageList.objects.get(pk=perm_id)
	if request.method == 'POST':	# no valid - just save
		stage = Stage.objects.get(pk=stage_id)
		# 1. delete all
		result = False
		try:
		#if (True):
			ps = PermitStage.objects.filter(stagelist=stagelist, stage=stage)
			if (ps):
				ps.delete()
			if (request.POST.get('g')):			# u'on' | None
				# 2. create new PermitStage
				ps = PermitStage(stagelist=stagelist, stage=stage)
				ps.save()
				for i in request.POST.getlist('id'):	# [u'<id>', ...]
					# 2.1 add jobs
					PermitStageJob(permitstage=ps, job=Job.objects.get(pk=i)).save()
		except:
			transaction.rollback()
		else:
			transaction.commit()
			result = True
		if (result):
			if (ps):	# FIXME:
				__log_it(request, ps, CHANGE)
				transaction.commit()
		return HttpResponseRedirect(reverse('sro2.views.stagelist_list', kwargs={ 'perm_id': perm_id }))	# FIXME:
	else:	# GET
		stage = Stage.objects.get(id=stage_id)
		mystages = PermitStage.objects.filter(stagelist=stagelist, stage=stage_id)
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
		return render_to_response('sro2/stagelist_edit_stage.html', RequestContext(request, { 'stagelist': stagelist, 'stage': stage, 'sflag': sflag, 'jobs': jobs }))

@login_required
def	stagelist_html(request, perm_id):
	return render_to_response('sro2/stagelist_html.html', RequestContext(request, { 'data': __load_permit(perm_id) }))

@login_required
def	stagelist_pdf(request, perm_id):
	data = __load_permit(perm_id)
	data['user'] = request.user.username
	return __pdf_render_to_response('sro2/permit.rml', {'data': data}, filename=data['stagelist'].permit.no + '.pdf')

@login_required
def	stagelist_dup(request, perm_id):
	if request.method == 'POST':
		form = StageListListForm(request.POST)
		if form.is_valid():
			type = form.cleaned_data['type']
			if (type):
				return HttpResponseRedirect(reverse('sro2.views.stagelist_dup_edit', kwargs={ 'perm_id': perm_id, 'type_id': type.id }))
	return HttpResponseRedirect(reverse('sro2.views.stagelist_list', kwargs={ 'perm_id': perm_id }))

@transaction.commit_manually
def	stagelist_dup_edit(request, perm_id, type_id):
	stagelist = StageList.objects.get(pk=perm_id)
	type = StageListType.objects.get(pk=type_id)
	type_id = int(type_id)
	needform = (StatementForm, PermitForm)[type_id - 1]
	if request.method == 'POST':
		form = needform(request.POST)
		if form.is_valid():
			result = False
			try:
			#if (True):
				# 1. main object
				new_stagelist = StageList(orgsro=stagelist.orgsro, type=type)
				new_stagelist.save()
				# 2. subobject
				if (type_id == 1):
					a = Statement(
						stagelist=new_stagelist,
						date=form.cleaned_data['date']
					)
				else:	# (type_id == 2):
					a = Permit(
						stagelist=new_stagelist,
						no=form.cleaned_data['no'],
						date=form.cleaned_data['date'],
						protocol=form.cleaned_data['protocol']
					)
				a.save()
				# 3. copy jobs
				for ps in stagelist.permitstage_set.all():
					permitstage = PermitStage(stagelist=new_stagelist, stage=ps.stage)
					permitstage.save()
					for psj in ps.permitstagejob_set.all():
						PermitStageJob(permitstage=permitstage, job=psj.job).save()
			except:
				transaction.rollback()
			#	return HttpResponseRedirect('../../')
			else:
				transaction.commit()
				result = True
			if (result):
				__log_it(request, a, ADDITION)
				transaction.commit()
			return HttpResponseRedirect(reverse('sro2.views.stagelist_list', kwargs={ 'perm_id': new_stagelist.id }))
	else:
		form = needform()
	return render_to_response('sro2/orgsro_stagelist_add.html', RequestContext(request, {'orgsro': stagelist.orgsro, 'type': type, 'form': form}))

@login_required
def	stagelist_cmp(request, perm_id):
	pass

@login_required
def	protocol_list(request, sro_id):
	return render_to_response('sro2/dummy.html', context_instance=RequestContext(request, {'sro': Sro.objects.get(pk=sro_id)}))
