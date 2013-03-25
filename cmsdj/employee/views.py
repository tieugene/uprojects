# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Sum, F
from django.shortcuts import redirect   #, render_to_response
from django.views.decorators.csrf import csrf_exempt
#from django.views.generic.simple import direct_to_template
#from django.views.generic.list_detail import object_list, object_detail
#from django.views.generic.create_update import create_object, update_object, delete_object

from jnj import *
import models, forms
from enum.models import DOW
from utils.pager import page_queryset, PAGE_SIZE
import svg

import datetime, pprint, calendar

def stafflist_list(request):
    return redirect('stafflist_view', models.StaffList.objects.order_by('begdate')[0].pk)
    #return jrender_to_response('employee/stafflist_list.html', {'object_list': models.StaffList.objects.order_by('begdate')}, request=request)

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
            roomed = 0
            doced = 0
            for i in specialty.rsentries.all():
                roomed += (i.endtime-i.begtime)
                for j in i.docs.all():
                    doced += (j.endtime-j.begtime)
            entry['roomed'] = roomed/2400.00 if roomed else 0   # 60 min * 40 h
            entry['doced'] = doced/2400.00 if doced else 0
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

def __time2min(time):
    return time.hour * 60 + time.minute

def __min2time(m):
    return datetime.time(m/60, m%60)

def rs_room_auto(request):
    return redirect('rs_room', models.RoomSchedule.objects.order_by('begdate')[0].pk, models.Room.objects.order_by('pk')[0].pk)

@csrf_exempt
def rs_room(request, rs_id, room_id):
    '''
    By cab (DxT=Spec) - ГКк
    View and add new rse
    @param rs_id:ID - RoomSchedule object id
    @param room_id:ID - Room object id
    '''
    schedule = models.RoomSchedule.objects.get(pk=int(rs_id))
    room = models.Room.objects.get(pk=int(room_id))
    if request.method == 'POST':
        form = forms.RSERoomForm(request.POST)
        if form.is_valid():
            models.RoomScheduleEntry.objects.create(
                schedule    = schedule,
                room        = form.cleaned_data['room'],
                dow         = form.cleaned_data['dow'],
                specialty   = form.cleaned_data['specialty'],
                begtime     = __time2min(form.cleaned_data['begtime']),
                endtime     = __time2min(form.cleaned_data['endtime']),
            )
            form = forms.RSERoomForm(initial={'schedule': schedule, 'room': room})
    else:   # GET
        form = forms.RSERoomForm(initial={'schedule': schedule, 'room': room})
    return jrender_to_response(
        'employee/rs_room.html',
        {
            'rs':       schedule,
            'room':     room,
            'rooms':    models.Room.objects.order_by('pk'),
            'form_rse': form,
        },
        request=request
    )

@csrf_exempt
def rse_room(request, id):
    entry = models.RoomScheduleEntry.objects.get(pk=int(id))
    form_rse = None
    form_rsed = None
    if request.method == 'POST':
        if ('submit_rse' in request.POST):
            form_rse = forms.RSERoomForm(request.POST)
            if form_rse.is_valid():
                # TODO: check changes
                entry.dow       = form_rse.cleaned_data['dow']
                entry.specialty = form_rse.cleaned_data['specialty']
                entry.begtime   = __time2min(form_rse.cleaned_data['begtime'])
                entry.endtime   = __time2min(form_rse.cleaned_data['endtime'])
                entry.save()
        else:
            form_rsed = forms.RSEDForm(request.POST)
            if form_rsed.is_valid():
                models.RoomScheduleEntryDoc.objects.create(
                    rse        = entry,
                    doc         = form_rsed.cleaned_data['doc'],
                    begtime     = __time2min(form_rsed.cleaned_data['begtime']) - entry.begtime,
                    endtime     = __time2min(form_rsed.cleaned_data['endtime']) - entry.begtime,
                )
                form_rsed = None
    if (form_rse == None):
        form_rse = forms.RSERoomForm(initial={
            'id':       entry.id,
            'schedule': entry.schedule,
            'room':     entry.room,
            'dow':      entry.dow,
            'begtime':  entry.get_begtime(),
            'endtime':  entry.get_endtime(),
            'specialty':entry.specialty,
        })
    if (form_rsed == None):
        form_rsed = forms.RSEDForm(initial={'rse': entry,})
    return jrender_to_response(
        'employee/rse_room.html',
        {
            'rs':   entry.schedule,
            'rse':  entry,
            'room': entry.room,
            'rooms': models.Room.objects.order_by('pk'),
            'form_rse': form_rse,
            'form_rsed': form_rsed,
        },
        request=request
    )

def rse_room_del(request, id):
    entry = models.RoomScheduleEntry.objects.get(pk=int(id))
    rs_id = entry.schedule.pk
    room_id = entry.room.pk
    entry.delete()
    return redirect('rs_room', rs_id, room_id)

@csrf_exempt
def rsed_room(request, id):
    entry = models.RoomScheduleEntryDoc.objects.get(pk=int(id))
    if request.method == 'POST':
        form = forms.RSEDForm(request.POST)
        if form.is_valid():
            entry.doc       = form.cleaned_data['doc']
            entry.begtime   = __time2min(form.cleaned_data['begtime']) - entry.rse.begtime
            entry.endtime   = __time2min(form.cleaned_data['endtime']) - entry.rse.begtime
            entry.save()
            return redirect('rse_room', entry.rse.pk)
    else:   # GET
        form = forms.RSEDForm(initial={
            'id':       entry.id,
            'rse':      entry.rse,
            'doc':      entry.doc,
            'begtime':  entry.get_begtime(),
            'endtime':  entry.get_endtime(),
        })
    return jrender_to_response(
        'employee/rsed_room.html',
        {
            'rs':   entry.rse.schedule,
            'room': entry.rse.room,
            'rooms': models.Room.objects.order_by('pk'),
            'rse':  entry.rse,
            'rsed':  entry,
            'form_rsed': form,
        },
        request=request
    )

def rsed_room_del(request, id):
    entry = models.RoomScheduleEntryDoc.objects.get(pk=int(id))
    rse_id = entry.rse.pk
    entry.delete()
    return redirect('rse_room', rse_id)

def rs_dow_auto(request):
    return redirect('rs_dow', models.RoomSchedule.objects.order_by('begdate')[0].pk, DOW.objects.order_by('pk')[0].pk)

@csrf_exempt
def rs_dow(request, rs_id, dow_id):
    '''
    * by day (CxT=Spec) - ГКд
    @param rs_id:ID - RoomSchedule object id
    @param room_id:ID - Room object id
    '''
    schedule = models.RoomSchedule.objects.get(pk=int(rs_id))
    dow = DOW.objects.get(pk=int(dow_id))
    rses = models.RoomScheduleEntry.objects.filter(schedule=schedule, dow=dow)
    if request.method == 'POST':
        form = forms.RSEDOWForm(request.POST)
        if form.is_valid():
            models.RoomScheduleEntry.objects.create(
                schedule    = schedule,
                room        = form.cleaned_data['room'],
                dow         = form.cleaned_data['dow'],
                specialty   = form.cleaned_data['specialty'],
                begtime     = __time2min(form.cleaned_data['begtime']),
                endtime     = __time2min(form.cleaned_data['endtime']),
            )
            form = forms.RSEDOWForm(initial={'schedule': schedule, 'dow': dow})
    else:   # GET
        form = forms.RSEDOWForm(initial={'schedule': schedule, 'dow': dow})
    return jrender_to_response(
        'employee/rs_dow.html',
        {
            'rs':   schedule,
            'dow':  dow,
            'dows': DOW.objects.order_by('pk'),
            'form_rse': form,
        },
        request=request
    )

@csrf_exempt
def rse_dow(request, id):
    entry = models.RoomScheduleEntry.objects.get(pk=int(id))
    form_rse = None
    form_rsed = None
    if request.method == 'POST':
        if ('submit_rse' in request.POST):
            form_rse = forms.RSEDOWForm(request.POST)
            if form_rse.is_valid():
                # TODO: check changes
                entry.room      = form_rse.cleaned_data['room']
                entry.specialty = form_rse.cleaned_data['specialty']
                entry.begtime   = __time2min(form_rse.cleaned_data['begtime'])
                entry.endtime   = __time2min(form_rse.cleaned_data['endtime'])
                entry.save()
        else:
            form_rsed = forms.RSEDForm(request.POST)
            if form_rsed.is_valid():
                models.RoomScheduleEntryDoc.objects.create(
                    rse        = entry,
                    doc         = form_rsed.cleaned_data['doc'],
                    begtime     = __time2min(form_rsed.cleaned_data['begtime']) - entry.begtime,
                    endtime     = __time2min(form_rsed.cleaned_data['endtime']) - entry.begtime,
                )
                form_rsed = None
    if (form_rse == None):
        form_rse = forms.RSEDOWForm(initial={
            'id':       entry.id,
            'schedule': entry.schedule,
            'room':     entry.room,
            'dow':      entry.dow,
            'begtime':  entry.get_begtime(),
            'endtime':  entry.get_endtime(),
            'specialty':entry.specialty,
        })
    if (form_rsed == None):
        form_rsed = forms.RSEDForm(initial={'rse': entry,})
    return jrender_to_response(
        'employee/rse_dow.html',
        {
            'rs':   entry.schedule,
            'rse':  entry,
            'dow':  entry.dow,
            'dows': DOW.objects.order_by('pk'),
            'form_rse': form_rse,
            'form_rsed': form_rsed,
        },
        request=request
    )

def rse_dow_del(request, id):
    entry = models.RoomScheduleEntry.objects.get(pk=int(id))
    rs_id = entry.schedule.pk
    dow_id = entry.dow.pk
    entry.delete()
    return redirect('rs_dow', rs_id, dow_id)

@csrf_exempt
def rsed_dow(request, id):
    entry = models.RoomScheduleEntryDoc.objects.get(pk=int(id))
    if request.method == 'POST':
        form = forms.RSEDForm(request.POST)
        if form.is_valid():
            entry.doc       = form.cleaned_data['doc']
            entry.begtime   = __time2min(form.cleaned_data['begtime']) - entry.rse.begtime
            entry.endtime   = __time2min(form.cleaned_data['endtime']) - entry.rse.begtime
            entry.save()
            return redirect('rse_dow', entry.rse.pk)
    else:   # GET
        form = forms.RSEDForm(initial={
            'id':       entry.id,
            'rse':      entry.rse,
            'doc':      entry.doc,
            'begtime':  entry.get_begtime(),
            'endtime':  entry.get_endtime(),
        })
    return jrender_to_response(
        'employee/rsed_dow.html',
        {
            'rs':   entry.rse.schedule,
            'dow': entry.rse.dow,
            'dows': DOW.objects.order_by('pk'),
            'rse':  entry.rse,
            'rsed':  entry,
            'form_rsed': form,
        },
        request=request
    )

def rsed_dow_del(request, id):
    entry = models.RoomScheduleEntryDoc.objects.get(pk=int(id))
    rse_id = entry.rse.pk
    entry.delete()
    return redirect('rse_dow', rse_id)

def employee_list(request):
    return jrender_to_response(
        'employee/employee_list.html', {
            'object_list': page_queryset(models.Employee.objects.all(), request.GET.get('page', 1)),
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

def ticket_list(request):
    return jrender_to_response(
        'employee/ticket_list.html', {
            'object_list': page_queryset(models.Ticket.objects.all(), request.GET.get('page', 1)),
        },
        request=request
    )

def ticket_view(request, id):
    return jrender_to_response(
        'employee/ticket_detail.html', {
            'object': models.Ticket.objects.get(pk=int(id)),
        },
        request=request
    )

def ticket_table_auto(request):
    '''
    @param yymmdd
    @param spec_id
    '''
    id = models.Specialty.objects.order_by('name')[0].pk
    yymmdd = datetime.date.today().strftime('%y%m%d')
    return redirect('ticket_table', id, yymmdd)

@csrf_exempt
def ticket_table(request, id, date):
    '''
    @param spec_id:int - specialty id
    @param yymmdd:date - date to show
    '''
    y, m, d = (2000+int(date[:2]), int(date[2:4]), int(date[4:]))
    cur_day = datetime.date(y, m, d)
    spec = models.Specialty.objects.get(pk=int(id))
    if request.method == 'POST':
        if ('submit_spec' in request.POST):
            form = forms.Specialty(request.POST)
            if form.is_valid():
                return redirect('ticket_table', form.cleaned_data['specialty'].pk, date)
    return jrender_to_response(
        'employee/ticket_table.html', {
            'spec': spec,
            'date': cur_day,
            'cal':  calendar.Calendar(),   # FIXME:
            'form_spec': forms.Specialty(initial={'specialty': spec}),
            'form_ticket': forms.Ticket(),
        },
        request=request
    )
