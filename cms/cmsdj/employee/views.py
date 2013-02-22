# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, delete_object

import models, forms

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
    need = dict()
    for i in sl.staves.all():
        #print i
        need[i.specialty.id] = i    # Specialty.id: StaffListEntry
    #need = dict(sl.staves.values_list('specialty_id', 'qty'))
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
            entry = {'spec': specialty}
            if specialty.id in need:
                entry['need'] = need[specialty.id]
            if specialty.id in are:
                entry['are'] = are[specialty.id]
            subdata.append(entry)
        data.append({'dep': department, 'data': subdata})
    return render_to_response('employee/stafflist_detail.html', {'stafflist': sl, 'data': data})

@csrf_exempt
def staff_add(request, list_id, spec_id):
    sl = models.StaffList.objects.get(pk=int(list_id))
    spec = models.Specialty.objects.get(pk=int(spec_id))
    if request.method == 'POST':
        form = forms.StaffForm(request.POST)
        if form.is_valid():
            models.StaffListEntry.objects.create(stafflist=sl, specialty=spec, qty=form.cleaned_data['qty'])
            return redirect('stafflist_view', list_id)
    else:
        form=forms.StaffForm()
    return render_to_response(
        'employee/staff_add.html',
        {
            'form': form,
            'stafflist': sl,
            'spec': spec,
        }
    )

@csrf_exempt
def staff_edit(request, id):
    sle = models.StaffListEntry.objects.get(pk=int(id))
    if request.method == 'POST':
        form = forms.StaffForm(request.POST)
        if form.is_valid():
            sle.qty = form.cleaned_data['qty']
            sle.save()
            return redirect('stafflist_view', sle.stafflist.pk)
    else:
        form=forms.StaffForm(initial={'qty': sle.qty})
    return render_to_response(
        'employee/staff_edit.html',
        {
            'form': form,
            'sle': sle,
        }
    )

def staff_del(request, id):
    staff = models.StaffListEntry.objects.get(pk=int(id))
    sl = staff.stafflist
    staff.delete()
    return redirect('stafflist_view', sl.pk)

def roomschedule_list(request):
	return  object_list (
		request,
		queryset = models.RoomSchedule.objects.order_by('begdate'),
	)

def roomschedule_view(request, id):
    rs = models.RoomSchedule.objects.get(pk=int(id))
    return render_to_response('employee/roomschedule_detail.html', {'begdate': rs.begdate})

def rse_add(request, id):
    return  create_object (request, model = models.Person, extra_context = {'cancelurl': reverse('person_list')})

def rse_edit(request, id):
    return  update_object (request, model = models.Person, object_id = id, extra_context = {'cancelurl': reverse('person_detail', args=[id,])})

def rse_del(request, id):
    models.Person.objects.get(pk=int(id)).delete()
    return redirect('person_list')

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
