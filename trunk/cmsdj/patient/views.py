# -*- coding: utf-8 -*-

from django.conf import settings
#from django.views.generic.simple import direct_to_template
#from django.views.generic.list_detail import object_list, object_detail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from jnj import *
from utils.pager import page_queryset
import models

def patient_list(request):
    return jrender_to_response('patient/patient_list.html', {
        'object_list': page_queryset(models.Patient.objects.all(), request.GET.get('page', 1)),
    }, request=request)

def patient_detail(request, id):
    return jrender_to_response('patient/patient_detail.html', {'object': models.Patient.objects.get(pk=int(id))}, request=request)

def patient_create(request):
    pass

def patient_update(request, id):
    pass

def patient_delete(request, id):
    pass
