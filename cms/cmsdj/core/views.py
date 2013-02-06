# -*- coding: utf-8 -*-

from django.conf import settings
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

@csrf_exempt
def person_create(request):
	return  create_object (
		request,
        model = models.Person,
        template_name = 'core/person_main_form.html',
	)

def person_delete(request, id):
    pass

def person_detail(request, id):
	return  object_detail (
		request,
		queryset = models.Person.objects.all(),
		object_id = id,
	)

def person_update_main(request, id):
	return  object_detail (
		request,
		queryset = models.Person.objects.all(),
		object_id = id,
	)
