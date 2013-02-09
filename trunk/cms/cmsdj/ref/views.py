# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

import models

PAGE_SIZE = 20

def index(request):
    return direct_to_template(request, 'ref/index.html')

def pmu_list(request):
	return  object_list (
		request,
		queryset = models.PMU3.objects.order_by('pk'),
        template_name = 'ref/pmu_list.html',
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
	)
