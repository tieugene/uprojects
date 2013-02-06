# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

import models

PAGE_SIZE = 20

def index(request):
    return direct_to_template(request, 'core/index.html')

# Person CRUD
def person_list(request):
	return  object_list (
		request,
		queryset = models.Person.objects.all(),
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
	)

def person_detail(request, id):
	return  object_detail (
		request,
		queryset = models.Person.objects.all(),
		object_id = id,
	)

# Person
def person_delete(request, id):
    models.Person.objects.get(pk=int(id)).delete()
    return redirect('person_list')

def person_create(request):
	return  create_object (request, model = models.Person)

def person_update(request, id):
	return  update_object (request, model = models.Person, object_id = id, extra_context = {'next': reverse('person_detail', args=[id,])})

# PersonAddress
def personaddress_delete(request, id):
    models.PersonAddress.objects.get(pk=int(id)).delete()
    return redirect('person_detail')

def personaddress_create(request, id):
	return  create_object (request, model = models.PersonAddress)

def personaddress_update(request, id):
	return  update_object (request, model = models.PersonAddress, object_id = id, extra_context = {'next': reverse('person_detail', args=[id,])})
