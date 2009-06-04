# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.db import transaction

from models import *
from forms import DbAclForm, UserAclForm, ImportForm

def	__updatesn():
	'''
	Increments sn variable in db
	'''
	sn = Var.objects.get(name="sn")
	if (sn):
		sn.value += 1
	else:
		sn = Var(name="sn", value=0)
	sn.save()

def	index(request):
	db_list = Db.objects.all().order_by('org')
	user_list = User.objects.all().order_by('login')
	return render_to_response('run1s/index.html', {'db_list': db_list, 'user_list': user_list,})

def	dbacl(request, db_id):
	db = Db.objects.get(pk=db_id)
	if request.method == 'POST':
		User.objects.get(pk=request.POST['user_id']).dbs.add(db)
		__updatesn()
	users = User.objects.exclude(dbs = db_id)
	return render_to_response('run1s/db_acl.html', {'db': db, 'users': users})

def	dbacldel(request, user_id, db_id):
	return __acldel(user_id, db_id, '/run1s/dbacl/%d' % int(db_id))

def	useracl(request, user_id):
	user = User.objects.get(pk = user_id)
	if request.method == 'POST':
		user.dbs.add(Db.objects.get(pk=request.POST['db_id']))
		__updatesn()
	dbs = Db.objects.exclude(user = user_id)
	return render_to_response('run1s/user_acl.html', {'user': user, 'dbs': dbs})

def	useracldel(request, user_id, db_id):
	return __acldel(user_id, db_id, '/run1s/useracl/%d' % int(user_id))

def	__acldel(user_id, db_id, redirect):
	User.objects.get(pk=user_id).dbs.remove(Db.objects.get(pk=db_id))
	__updatesn()
	return HttpResponseRedirect(redirect)

def	__getsn():
	sn = Var.objects.get(name="sn")
	if (sn):
		return int(sn.value)
	else:
		return 0

def	sn(request):
	response = HttpResponse(mimetype='text/plain; charset=utf-8')
	response.write("sn\t%d" % __getsn())

def	listxml(request, login, password):
	response = sn(request)
	user = User.objects.get(login=login)
	t = loader.get_template('run1s/baselist.xml')
	err = None
	dbs = []
	if (user):
		if (user.password == password):
			dbs = user.dbs.all()
		else:
			err = "Wrong password"
	else:
		err = "Wrong login"
	xml = t.render(Context({'sn': __getsn(), 'err': err, 'dbs': dbs}))
	return HttpResponse(xml)

def	listtxt(request, login, password):
	response = sn(request)
	user = User.objects.get(login=login)
	if (user):
		if (user.password == password):
			for db in user.dbs.all():
				response.write(u'\ndb\t%s\t%s\t%s\t%s\t%s\t%s' % (db.share.host.name, db.share.name, db.path, db.org.name, db.type.name, db.comments))
		else:
			response.write("\nerror\twrong password")
	else:
		response.write("\nerror\twrong login")
	return response

def	importdb(request):
	if request.method == 'POST':
		form = ImportForm(request.POST, request.FILES)
		if form.is_valid():
			__updatesn()
			__handle_uploaded_file(request.FILES['file'])
			return HttpResponseRedirect('/run1s/')
	else:
		form = ImportForm()
	return render_to_response('run1s/import.html', {'form': form})

def	__handle_uploaded_file(f):
	# 1. load text
	text = ""
	for chunk in f.chunks():
		text += chunk
	# 2. load into inner
	user	= {}
	org	= {}
	dbtype	= {}
	host	= {}
	share	= {}
	db	= {}
	acl	= {}
	transaction.commit()
	try:
	#if (True):
		User.objects.all().delete()
		Org.objects.all().delete()
		Dbtype.objects.all().delete()
		Host.objects.all().delete()
		for i in text.splitlines():
			k = i.split("\t")
			if (k[0] == "user"):
				user[int(k[1])]	= User(login=k[2], password=k[3], comments=k[4])
				user[int(k[1])].save()
			elif (k[0] == "org"):
				org[int(k[1])]	= Org(name=k[2], comments=k[3])
				org[int(k[1])].save()
			elif (k[0] == "dbtype"):
				dbtype[int(k[1])] = Dbtype(name=k[2], comments=k[3])
				dbtype[int(k[1])].save()
			elif (k[0] == "host"):
				host[int(k[1])]	= Host(name=k[2], comments=k[3])
				host[int(k[1])].save()
			elif (k[0] == "share"):
				share[int(k[1])] = Share(host=host[int(k[2])], name=k[3], comments=k[4])
				share[int(k[1])].save()
			elif (k[0] == "db"):
				db[int(k[1])] = Db(share=share[int(k[2])], type=dbtype[int(k[3])], org=org[int(k[4])], path=k[5], comments=k[6])
				db[int(k[1])].save()
			elif (k[0] == "acl"):
				user[int(k[2])].dbs.add(db[int(k[3])])	# acl[user_id] = db
	except:
		transaction.rollback()
	else:
		transaction.commit()
