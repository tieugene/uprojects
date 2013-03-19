# -*- coding: utf-8 -*-

from django.conf import settings
#from django.views.generic.simple import direct_to_template
#from django.views.generic.list_detail import object_list, object_detail

from jnj import *
import models

PAGE_SIZE = 20

def patient_list(request):
    return jrender_to_response('patient/patient_list.html', {'object_list': models.Patient.objects.order_by('pk'),}, request=request)

def patient_detail(request, id):
    return jrender_to_response('patient/patient_detail.html', {'object': models.Patient.objects.get(pk=int(id))}, request=request)

def patient_create(request):
    pass

def patient_update(request, id):
    pass

def patient_delete(request, id):
    pass
