# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.shortcuts import redirect   #, render_to_response
from django.views.decorators.csrf import csrf_exempt
#from django.views.generic.simple import direct_to_template
#from django.views.generic.list_detail import object_list, object_detail
#from django.views.generic.create_update import create_object, update_object, delete_object

from jnj import *
import models, forms
from enum.models import DOW

PAGE_SIZE = 20

def index(request):
    return jrender_to_response('employee/index.html', request=request)

def stafflist_list(request):
    return jrender_to_response('employee/stafflist_list.html', {'object_list': models.StaffList.objects.order_by('begdate')}, request=request)

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
    return jrender_to_response('employee/stafflist_detail.html', {'stafflist': sl, 'data': data}, request=request)

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
    return jrender_to_response(
        'employee/staff_add.html',
        {
            'form': form,
            'stafflist': sl,
            'spec': spec,
        },
        request=request
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
    return jrender_to_response(
        'employee/staff_edit.html',
        {
            'form': form,
            'sle': sle,
        },
        request=request
    )

def staff_del(request, id):
    staff = models.StaffListEntry.objects.get(pk=int(id))
    sl = staff.stafflist
    staff.delete()
    return redirect('stafflist_view', sl.pk)

def roomschedule_list(request):
    room0 = models.Room.objects.order_by('pk')[0].pk
    dow0 = DOW.objects.order_by('pk')[0].pk
    return jrender_to_response(
        'employee/roomschedule_list.html',
        {
            'object_list': models.RoomSchedule.objects.order_by('begdate'),
            'room0': room0,
            'dow0': dow0,
        },
        request=request
    )

@csrf_exempt
def rs_room(request, rs_id, room_id, form=None):
    '''
    By cab (DxT=Spec) - ГКк
    @param rs_id:ID - RoomSchedule object id
    @param r_id:ID - Room object id
    TODO:
    Test: cab. #2, LOR (), Mon 540..720 (9:00-12:00)
    '''
    rs = models.RoomSchedule.objects.get(pk=int(rs_id))
    room = models.Room.objects.get(pk=int(room_id))
    rse = models.RoomScheduleEntry.objects.filter(schedule=rs, room=room)
    if request.method == 'POST':
        form = forms.RSEForm(request.POST, rs=rs, room=room)
        if form.is_valid():
            begtime=form.cleaned_data['begtime']
            endtime=form.cleaned_data['endtime']
            models.RoomScheduleEntry.objects.create(
                schedule=rs,
                room=room,
                specialty=form.cleaned_data['specialty'],
                dow=form.cleaned_data['dow'],
                begtime=begtime.hour*60+begtime.minute,
                endtime=endtime.hour*60+endtime.minute,
            )
            form = forms.RSEForm()
    else:
        form=forms.RSEForm()
    return jrender_to_response(
        'employee/rs_room.html',
        {
            'rs': rs,	# RoomSchedule
            'room': room,
            'rse': rse,
            'dows': DOW.objects.order_by('pk'),
            'rooms': models.Room.objects.order_by('pk'),
            'hbeg': 8,
            'hend': 22,
            'form': form,
        },
        request=request
    )

@csrf_exempt
def rse_room_edit(request, id):
    return  update_object (request, model = models.Person, object_id = id, extra_context = {'cancelurl': reverse('person_detail', args=[id,])})

def rse_room_del(request, id):
    models.Person.objects.get(pk=int(id)).delete()
    return redirect('person_list')

def rs_dow(request, rs_id, dow_id):
    '''
    * by day (CxT=Spec) - ГКд
    '''
    pass

def employee_list(request):
    return jrender_to_response(
        'employee/employee_list.html',
        {
            'object_list': models.Employee.objects.order_by('pk'),
        },
        request=request
    )

def employee_view(request, id):
    return jrender_to_response(
        'employee/employee_detail.html',
        {
            'object': models.Employee.objects.get(pk=int(id)),
        },
        request=request
    )
