# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

import models

PAGE_SIZE = 20

def index(request):
    return direct_to_template(request, 'patient/index.html')

def patient_list(request):
	return  object_list (
		request,
		queryset = models.Patient.objects.order_by('pk'),
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
	)

def patient_detail(request, id):
	return  object_detail (
		request,
		queryset = models.Patient.objects.all(),
		object_id = id,
	)
