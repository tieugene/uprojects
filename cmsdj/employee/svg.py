# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

import jnj
import models
from enum.models import DOW
import datetime, calendar

def __head(hx, hy, hbeg, hend):
    '''
    svg header
    '''
    dy = (100.0 - hy)/(hend - hbeg)   # per hour
    r = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" id="thesvg" height="100" onload="refresh_svg();">\n'
    r += '<rect id="svgbg" width="100%" height="100%"/>\n'
    r += '<g class="head">'
    r += '<line x1="0" y1="0" x2="%f%%" y2="%f%%"/>\n' % (hx, hy)
    # <!-- horizontal grid -->
    for row, h in enumerate(range(hend - hbeg)):
        y = hy + (row * dy)
        r += '<line x1="0" y1="%f%%" x2="100%%" y2="%f%%"/>\n' % (y, y)
        r += '<text x="0" y="%f%%"><tspan dy="1.5ex"> %02d:00 </tspan></text>\n' % (y, h + hbeg)
    r += '</g>'
    return r

def __headitem(x, dx, url, name):
    r  = '<g class="head">\n'
    r += '<line x1="%f%%" y1="0" y2="100%%" x2="%f%%"/>\n' % (x, x)
    r += '<g class="hcenter">\n'
    r += '<a xlink:href="%s">\n' % url
    r += '<text x="%f%%" y="0"> <tspan dy="1.5ex"> %s </tspan> </text>\n' % (x+(dx/2.0), name)
    r += '</a>\n'
    r += '</g>\n'
    r += '</g>\n'
    return r

def svg_room(room, highlight=None):
    '''
    rse=None: ok
    rse: rse=yellow, chg url1
    rsed: rsed=green, chg url2
    '''
    itsrse = bool(highlight) and isinstance(highlight, models.RoomScheduleEntry)
    itsrsed = bool(highlight) and isinstance(highlight, models.RoomScheduleEntryDoc)
    # prepare
    schedule = models.RoomSchedule.objects.order_by('begdate')[0].pk
    rses = models.RoomScheduleEntry.objects.filter(schedule=schedule, room=room)
    cols = DOW.objects.order_by('pk')
    col_e2n = dict()   # convert dow to column
    # go
    hx = 9
    hy = 9
    hbeg = 8
    hend = 22
    r = __head(hx, hy, hbeg, hend)
    dy = (100.0 - hy)/(hend - hbeg)   # per hour
    dx = (100.0 - hx)/cols.count()
    # <!-- vertical grid:  -->
    for col_n, col_e in enumerate(cols):
        col_e2n[col_e.pk] = col_n
        r += __headitem(hx + (col_n * dx), dx, reverse('rs_dow', args=[schedule, col_e.pk]), col_e.name)
    # room slots
    for entry in rses:
        thisrse = (itsrse and (highlight.id == entry.pk))
        x = hx + (col_e2n[entry.dow.pk] * dx)
        y = hy+(((entry.begtime/60.0)-hbeg)*dy)
        r += '<g class="occupy">\n'
        # rse_room && !rsed_room: if (rse == entry) => 'rs_room'(entry.schedule.pk, entry.room.pk) + yellow
        r += '<a xlink:href="%s">\n' % (reverse('rs_room', args=[entry.schedule.pk, entry.room.pk]) if (thisrse) else reverse('rse_room', args=[entry.pk,]))
        r += '<rect x="%f%%" y="%f%%" width="%f%%" height="%f%%" rx="3" ry="3" %s />\n' % (
            x, y, dx, (entry.endtime-entry.begtime)/60.0*dy, 'style="fill: yellow"' if (thisrse) else '')
        xt = x+(dx/2.0)
        r += '<text x="%f%%" y="%f%%">' % (xt, y)
        for t in entry.specialty.get_name_wrapped():
            r += '<tspan x="%f%%" dy="1.5ex"> %s </tspan>\n' % (xt, t)
        r += '</text>\n'
        r += '</a>\n'
        r += '</g>\n'
    # doctors
        r += '<g class="doccupy">\n'
        for doc in entry.docs.all():
            thisrsed = (itsrsed and (highlight.id == doc.pk))
            docy = hy+((((entry.begtime+doc.begtime)/60.0)-hbeg)*dy)
            # rsed_room: if (rsed == doc) => 'rse_room'(rse.pk) + green
            r += '<a xlink:href="%s">\n' % (reverse('rs_room', args=[entry.schedule.pk, entry.room.pk]) if (thisrsed) else reverse('rsed_room', args=[doc.pk]))
            r += '<rect x="%f%%" y="%f%%" width="%f%%" height="%f%%" rx="3" ry="3" %s />\n' % (
                xt, docy, dx/2.0, (doc.endtime-doc.begtime)/60.0*dy, 'style="fill: green"' if (thisrsed) else '')
            r += '<text x="%f%%" y="%f%%" dy="1em"> %s </text>\n' % (x+(dx*0.75), docy, doc.doc.person.lastname)
            r += '</a>\n'
        r += '</g>\n'
    # close
    r += '</svg>\n'
    return r

def svg_dow(dow, highlight=None):
    itsrse = bool(highlight) and isinstance(highlight, models.RoomScheduleEntry)
    itsrsed = bool(highlight) and isinstance(highlight, models.RoomScheduleEntryDoc)
    # prepare
    schedule = models.RoomSchedule.objects.order_by('begdate')[0].pk
    rses = models.RoomScheduleEntry.objects.filter(schedule=schedule, dow=dow)
    cols = models.Room.objects.order_by('pk')
    col_e2n = dict()   # convert room to column
    # go
    hx = 9
    hy = 9
    hbeg = 8
    hend = 22
    r = __head(hx, hy, hbeg, hend)
    dy = (100.0 - hy)/(hend - hbeg)   # per hour
    dx = (100.0 - hx)/cols.count()
    # <!-- vertical grid:  -->
    for col_n, col_e in enumerate(cols):
        col_e2n[col_e.pk] = col_n
        r += __headitem(hx + (col_n * dx), dx, reverse('rs_room', args=[schedule, col_e.pk]), '%02d' % col_e.pk)
    # room slots
    for entry in rses:
        thisrse = (itsrse and (highlight.id == entry.pk))
        x = hx + (col_e2n[entry.room.pk] * dx)
        y = hy+(((entry.begtime/60.0)-hbeg)*dy)
        r += '<g class="occupy">\n'
        r += '<a xlink:href="%s">\n' % (reverse('rs_dow', args=[entry.schedule.pk, entry.dow.pk]) if (thisrse) else reverse('rse_dow', args=[entry.pk,]))
        r += '<rect x="%f%%" y="%f%%" width="%f%%" height="%f%%" rx="3" ry="3" %s />\n' % (
            x, y, dx, (entry.endtime-entry.begtime)/60.0*dy, 'style="fill: yellow"' if (thisrse) else '')
        xt = x+(dx/2.0)
        r += '<text x="%f%%" y="%f%%">' % (xt, y)
        for t in entry.specialty.get_name_wrapped():
            r += '<tspan x="%f%%" dy="1.5ex"> %s </tspan>\n' % (xt, t)
        r += '</text>\n'
        r += '</a>\n'
        r += '</g>\n'
    # doctors
        r += '<g class="doccupy">\n'
        for doc in entry.docs.all():
            thisrsed = (itsrsed and (highlight.id == doc.pk))
            docy = hy+((((entry.begtime+doc.begtime)/60.0)-hbeg)*dy)
            r += '<a xlink:href="%s">\n' % (reverse('rs_dow', args=[entry.schedule.pk, entry.dow.pk]) if (thisrsed) else reverse('rsed_dow', args=[doc.pk]))
            r += '<rect x="%f%%" y="%f%%" width="%f%%" height="%f%%" rx="3" ry="3" %s />\n' % (
                xt, docy, dx/2.0, (doc.endtime-doc.begtime)/60.0*dy, 'style="fill: green"' if (thisrsed) else '')
            r += '<text x="%f%%" y="%f%%" dy="1em"> %s </text>\n' % (x+(dx*0.75), docy, doc.doc.person.lastname)
            r += '</a>\n'
        r += '</g>\n'
    # close
    r += '</svg>\n'
    return r

def svg_tickets(spec, date, tick=None):
    '''
    Draw svg for tickets table.
    @param spec:Specialty - subj
    @param date:date - date
    '''
    schedule = models.RoomSchedule.objects.order_by('begdate')[0].pk
    rses = models.RoomScheduleEntry.objects.filter(schedule=schedule, specialty=spec)
    rooms_pk = set(rses.values_list('room__pk', flat=True))
    cols = models.Room.objects.filter(pk__in = rooms_pk).order_by('pk')
    if (cols.count() < 1):
        return '<p style="text-align: center"> Nothing to do </p>'
    col_e2n = dict()   # convert room to column
    hx = 9
    hy = 9
    hbeg = 8
    hend = 22
    r = __head(hx, hy, hbeg, hend)
    dy = (100.0 - hy)/(hend - hbeg)   # per hour
    dx = (100.0 - hx)/cols.count()
    # <!-- vertical grid:  -->
    for col_n, col_e in enumerate(cols):
        col_e2n[col_e.pk] = col_n
        r += __headitem(hx + (col_n * dx), dx, '...', '%02d' % col_e.pk)
    # available slots
    r += '<g class="occupy">\n'
    for rse in rses.filter(dow__pk=date.isoweekday()):
        for rsed in rse.docs.all():
            x = hx + (col_e2n[rse.room.pk] * dx)
            y = hy + ((((rse.begtime+rsed.begtime)/60.0)-hbeg)*dy)
            h = (rsed.endtime-rsed.begtime)/60.0*dy
            r += '<a xlink:href="_add_ticket_">\n<rect x="%f%%" y="%f%%" width="%f%%" height="%f%%" rx="3" ry="3" />\n</a>\n' % (x, y, dx, h)
    r += '</g>\n'
    # busy (TODO:: col2x, min2y)
    r += '<g class="doccupy">\n'
    backurl = reverse('ticket_table', args=[spec.pk, date.strftime('%y%m%d')])
    for ticket in models.Ticket.objects.filter(specialty=spec, date=date):
        thisticket = bool(tick) and (ticket == tick)
        x = hx + (col_e2n[ticket.room.pk] * dx)
        #y = hy + (((ticket.begtime/60.0)-hbeg)*dy)
        #h = (ticket.endtime-ticket.begtime)/60.0*dy
        y = hy + ((ticket.begtime.hour+(ticket.begtime.minute/60.0)-hbeg)*dy)
        h = ((ticket.endtime.hour-ticket.begtime.hour)+(ticket.endtime.minute-ticket.begtime.minute)/60.0)*dy
        r += '<a xlink:href="%s">\n' % ( backurl if thisticket else reverse('ticket', args=[ticket.pk]))
        r += '<rect x="%f%%" y="%f%%" width="%f%%" height="%f%%" rx="3" ry="3" %s />\n' % (x, y, dx, h, 'style="fill: yellow"' if (thisticket) else '')
        r += '</a>\n'
        #print ticket.patient
    r += '</g>\n'
    # close
    r += '</svg>\n'
    return r

jnj.env.globals['svg_room'] = svg_room
jnj.env.globals['svg_dow'] = svg_dow
jnj.env.globals['svg_tickets'] = svg_tickets
