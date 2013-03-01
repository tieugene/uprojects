# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
import decimal, datetime

import models

mintime = datetime.time(8)
maxtime = datetime.time(22)

class   StaffForm(forms.Form):
    qty = forms.DecimalField(min_value=decimal.Decimal('0.01'), max_digits=5, decimal_places=2)

class   RSEForm(forms.Form):
    '''
    TODO:
    * room > dep > specs only
    * beg, end - time widget
    Check:
    * time min/max
    * [in this RS] this cab is free for dow x (beg..end); else: <занед>
    PreSave: convert HH:MM into minutes
    '''
    #schedule	= forms.ModelChoiceField(RoomSchedule, related_name='entries', verbose_name=u'ГК')
    #room	= forms.ForeignKey(Room, related_name='+', verbose_name=u'Кабинет')
    dow         = forms.ModelChoiceField(models.DOW.objects.all(), label='День', empty_label=None)
    begtime     = forms.TimeField(label='с', widget=forms.widgets.TimeInput(format='%h:%M'))
    endtime     = forms.TimeField(label='по')
    specialty   = forms.ModelChoiceField(models.Specialty.objects.all(), label='Специальность', empty_label=None)

    def __init__(self, *args, **kwargs):
        self.rs = kwargs.pop('rs') if 'rs' in kwargs else None
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
            if (models.RoomScheduleEntry.objects.filter(schedule=self.rs, room=self.room, dow=cleaned_data.get('dow'), begtime__lt=endmin, endtime__gt=begmin).count()):
                raise forms.ValidationError("%d intersected sockets!" % x)
        return cleaned_data

class   RSEModelForm(forms.ModelForm):
    class   Meta:
        model = models.RoomScheduleEntry
