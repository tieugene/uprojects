# -*- coding: utf-8 -*-

from django.conf import settings
#from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

from jnj import *
import models

PAGE_SIZE = 20

def index(request):
    return jrender_to_response('ref/index.html', request=request)

def pmu_list(request):
    '''
    TODO: pager
    '''
    return jrender_to_response('ref/pmu_list.html', {'object_list': models.PMU3.objects.order_by('pk'),}, request=request)
