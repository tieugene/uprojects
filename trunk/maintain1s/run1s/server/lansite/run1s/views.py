# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from models import Db, User
from forms import DbAclForm

def	index(request):
	db_list = Db.objects.all().order_by('org')
	user_list = User.objects.all().order_by('login')
	return render_to_response('run1s/index.html', {'db_list': db_list, 'user_list': user_list,})

def	dbacl(request, db_id):
	db = Db.objects.get(pk=db_id)
	#form = DbAclForm()
	return render_to_response('run1s/db_acl.html', {'db': db})
	#return render_to_response('run1s/db_acl.html', {''})

def	useracl(request, user_id):
	user = User.objects.get(pk=user_id)
	dbs = Db.objects.all()
	return render_to_response('run1s/user_acl.html', {'user': user, 'dbs': dbs})
