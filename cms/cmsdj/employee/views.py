# -*- coding: utf-8 -*-

from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail

import models

PAGE_SIZE = 20

def index(request):
    return direct_to_template(request, 'employee/index.html')

def stafflist_list(request):
	return  object_list (
		request,
		queryset = models.StaffList.objects.order_by('begdate'),
	)

def stafflist_view(request, id):
    '''
    По всем отделениям
    По всем специальностям оного
    qty
    и сумма по врачам
    => тупо заполнить список ((dep, (spec, qty, ready)), )
    '''
    # 1. load wanted (StaffListEntry => specialty.id: qty)
    sl = models.StaffList.objects.get(pk=int(id))
    need = dict(sl.staves.values_list('specialty_id', 'qty'))
    # 2. load exists (EmployeeSpecialty => specialty.id, Sum(rate)
    #are = models.EmployeeSpecialty.objects.values('specialty_id')  #.annotate(total=Sum('rate')).order_by()
    are = {}
    for i in models.EmployeeSpecialty.objects.all():
        if (i.rate):
            are[i.specialty.id] = are.get(i.specialty.id, 0) + i.rate
    # 3. go
    data = list()
    for department in models.Department.objects.all():
        subdata = list()
        for specialty in department.specialties.all():
            subdata.append({'name': specialty.name, 'need': need.get(specialty.id, '-'), 'are': are.get(specialty.id, '-')})
        data.append({'name': department.name, 'data': subdata})
    return render_to_response('employee/stafflist_detail.html', {'begdate': sl.begdate, 'data': data})

def staff_add(request, id):
    pass

def staff_edit(request, id):
    pass

def staff_del(request, id):
    pass

def employee_list(request):
	return  object_list (
		request,
		queryset = models.Employee.objects.order_by('pk'),
		paginate_by = PAGE_SIZE,
		page = int(request.GET.get('page', '1')),
	)

def employee_view(request, id):
	return  object_detail (
		request,
		queryset = models.Employee.objects.all(),
		object_id = id,
	)
