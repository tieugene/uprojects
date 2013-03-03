# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
import decimal, datetime

import models

mintime = datetime.time(8)
maxtime = datetime.time(22)

class   StaffForm(forms.Form):
    qty = forms.DecimalField(min_value=decimal.Decimal('0.01'), max_digits=5, decimal_places=2)

class   RSEModelForm(forms.ModelForm):
    class   Meta:
        model = models.RoomScheduleEntry

class   RSEForm_old(forms.Form):
    '''
    TODO:
    * room > dep > specs only
    * beg, end - time widget
    Check:
    * time min/max
    * [in this RS] this cab is free for dow x (beg..end); else: <занед>
    PreSave: convert HH:MM into minutes
    '''
    #id          = forms.IntegerField(label='ID', required=False)
    #schedule	= forms.ModelChoiceField(models.RoomSchedule, label='ГК')
    #room	    = forms.ModelChoiceField(models.Room, label='Кабинет')
    dow         = forms.ModelChoiceField(models.DOW.objects.all(), label='День', empty_label=None)
    begtime     = forms.TimeField(label='с', widget=forms.widgets.TimeInput(format='%h:%M'))
    endtime     = forms.TimeField(label='по')
    specialty   = forms.ModelChoiceField(models.Specialty.objects.all(), label='Специальность', empty_label=None)

    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop('schedule') if 'schedule' in kwargs else None
        self.room = kwargs.pop('room') if 'room' in kwargs else None
        super(RSEForm, self).__init__(*args, **kwargs)

    def clean_begtime(self):
            data = self.cleaned_data['begtime']
            if (data):
                if data < mintime:
                    raise forms.ValidationError("Can't be < 08:00!")
                if data >= maxtime:
                    raise forms.ValidationError("Can't be >= 22:00!")
            return data

    def clean_endtime(self):
            data = self.cleaned_data['endtime']
            if (data):
                if data <= mintime:
                    raise forms.ValidationError("Can't be <= 08:00!")
                if data > maxtime:
                    raise forms.ValidationError("Can't be > 22:00!")
            return data

    def clean(self):
        cleaned_data = super(RSEForm, self).clean()
        begtime = cleaned_data.get('begtime')
        endtime = cleaned_data.get('endtime')
        if (begtime) and (endtime):
            if (begtime >= endtime):
                raise forms.ValidationError("Begtime >= Endtime!")
            begmin = begtime.hour * 60 + begtime.minute
            endmin = endtime.hour * 60 + endtime.minute
            x = (models.RoomScheduleEntry.objects.filter(schedule=self.schedule, room=self.room, dow=cleaned_data.get('dow'), begtime__lt=endmin, endtime__gt=begmin).count())
            if x:
                raise forms.ValidationError("%d intersected sockets!" % x)
        return cleaned_data

class   RSEForm(forms.Form):
    '''
    '''
    id          = forms.IntegerField(label='ID', required=False, widget = forms.HiddenInput())
    schedule	= forms.ModelChoiceField(models.RoomSchedule.objects, label='ГК', empty_label=None, widget = forms.HiddenInput())
    room	    = forms.ModelChoiceField(models.Room.objects, label='Кабинет', empty_label=None, widget = forms.HiddenInput())
    dow         = forms.ModelChoiceField(models.DOW.objects, label='День', empty_label=None)
    begtime     = forms.TimeField(label='с', widget=forms.widgets.TimeInput(format='%H:%M'))
    endtime     = forms.TimeField(label='по', widget=forms.widgets.TimeInput(format='%H:%M'))
    specialty   = forms.ModelChoiceField(models.Specialty.objects, label='Специальность', empty_label=None)

    #def __init__(self, *args, **kwargs):
    #    super(RSEForm, self).__init__(*args, **kwargs)

    def clean_begtime(self):
            data = self.cleaned_data['begtime']
            if (data):
                if (data < mintime) or (data >= maxtime):
                    raise forms.ValidationError('Must be 08:00..22:00')
            return data

    def clean_endtime(self):
            data = self.cleaned_data['endtime']
            if (data):
                if (data < mintime) or (data >= maxtime):
                    raise forms.ValidationError('Must be 08:00..22:00')
            return data

    def clean(self):
        cleaned_data = super(RSEForm, self).clean()
        begtime = cleaned_data.get('begtime')
        endtime = cleaned_data.get('endtime')
        if (begtime) and (endtime):
            if (begtime >= endtime):
                raise forms.ValidationError('Begtime >= Endtime!')
            begmin = begtime.hour * 60 + begtime.minute
            endmin = endtime.hour * 60 + endtime.minute
            x = (models.RoomScheduleEntry.objects.filter(
                schedule=cleaned_data['schedule'],
                room=cleaned_data['room'],
                dow=cleaned_data.get('dow'),
                begtime__lt=endmin,
                endtime__gt=begmin)
            )
            if (cleaned_data['id']):
                x = x.exclude(id=cleaned_data['id'])
            x = x.count()
            if x:
                raise forms.ValidationError("%d intersected sockets!" % x)
        return cleaned_data
