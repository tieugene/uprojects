# -*- coding: utf-8 -*-
from django import forms
import decimal

import models

class   StaffForm(forms.Form):
    qty = forms.DecimalField(min_value=decimal.Decimal('0.01'), max_digits=5, decimal_places=2)

class   RSEForm(forms.Form):
    '''
    TODO:
    * room > dep > specs only
    * spec - not null
    * dow - not null
    * beg, end - time widget
    * room - show, fix
    Check:
    * [in this RS] this cab is free for dow x (beg..end); else: <занед>
    PreSave: convert HH:MM into minutes
    '''
    #schedule	= forms.ModelChoiceField(RoomSchedule, related_name='entries', verbose_name=u'ГК')
    #room	= forms.ForeignKey(Room, related_name='+', verbose_name=u'Кабинет')
    dow         = forms.ModelChoiceField(models.DOW.objects.all(), label='День')
    begtime     = forms.TimeField(label='с', widget=forms.widgets.TimeInput(format='%h:%M'))
    endtime     = forms.TimeField(label='по')
    specialty   = forms.ModelChoiceField(models.Specialty.objects.all(), label='Специальность')
#forms.DateField(input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.widgets.DateTimeInput(format='%d.%m.%Y'), label='Дата рождения', required=False)
