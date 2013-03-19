# -*- coding: utf-8 -*-

from django.conf import settings
#from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

from jnj import *
from utils.pager import page_queryset
import models

def pmu_list(request):
    return jrender_to_response('ref/pmu_list.html', {
        'object_list': page_queryset(models.PMU3.objects.order_by('pk'), request.GET.get('page', 1)),
    }, request=request)
