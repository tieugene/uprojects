# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

import models, forms

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
	return  create_object (request, model = models.Person, extra_context = {'cancelurl': reverse('person_list')})

def person_update(request, id):
	return  update_object (request, model = models.Person, object_id = id, extra_context = {'cancelurl': reverse('person_detail', args=[id,])})

# PersonAddress
def personaddress_delete(request, id):
    object = models.PersonAddress.objects.get(pk=int(id))
    person = object.person
    object.delete()
    return redirect('person_detail', args=[person.pk,])

def personaddress_create(request, id):
    person = models.Person.objects.get(pk=int(id))
    #return  create_object (request, model = models.PersonAddress)
    return  create_object (request, form_class = forms.PersonAddressForm, extra_context = {'cancelurl': reverse('person_detail', args=[person.pk,])})

def personaddress_update(request, id):
    object = models.PersonAddress.objects.get(pk=int(id))
    person = object.person
    return  update_object (request, model = models.PersonAddress, object_id = id, extra_context = {'cancelurl': reverse('person_detail', args=[person.pk,])})
