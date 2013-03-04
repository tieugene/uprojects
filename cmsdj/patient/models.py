# -*- coding: utf-8 -*-
'''
Patient > MedHistory > Visit > MedRecord > MedRecordEntry
'''

from django.db import models
from django.conf import settings

from core.models import Person
from employee.models import Employee

class   Patient(models.Model):
    person      = models.OneToOneField(Person, verbose_name=u'Людь')
    nationality = models.CharField(max_length=32, blank=True, verbose_name=u'Национальность')
    deathdate   = models.DateField(null=True, blank=True, verbose_name=u'Дата смертии')

    class   Meta:
        ordering                = ('person', )
        verbose_name            = u'Поциэнт'
        verbose_name_plural     = u'Поциэнты'

    def     __unicode__(self):
        return str(self.person)

    @models.permalink
    def get_absolute_url(self):
        return ('patient_detail', (), {'id': self.pk})

class   MedHistory(models.Model):
    patient     = models.ForeignKey(Patient, related_name='medhistories', verbose_name=u'Поциэнт')
    date_from   = models.DateField(verbose_name=u'Дата начала')
    date_till   = models.DateField(null=True, blank=True, verbose_name=u'Дата окончания')

    class   Meta:
        verbose_name            = u'История болезни'
        verbose_name_plural     = u'Истории болезни'

class   Visit(models.Model):
    medhistory  = models.ForeignKey(MedHistory, related_name='visits', verbose_name=u'История болезни')
    date        = models.DateField(verbose_name=u'Дата посещения')
    active      = models.BooleanField(verbose_name=u'Актив')

    class   Meta:
        verbose_name            = u'Посещение'
        verbose_name_plural     = u'Посещения'

class   MedRecord(models.Model):
    visit       = models.ForeignKey(Visit, related_name='medrecords', verbose_name=u'Посещение')
    employee    = models.ForeignKey(Employee, related_name='medrecords', verbose_name=u'Врач')

    class   Meta:
        verbose_name            = u'МедЗапись'
        verbose_name_plural     = u'МедЗаписи'

class   MedRecordEntry(models.Model):
    medrecord   = models.ForeignKey(MedRecord, related_name='entries', verbose_name=u'Мед. запись')
    name        = models.CharField(max_length=32, verbose_name=u'Наименование')
    value       = models.CharField(max_length=32, verbose_name=u'Значение')
    unit        = models.CharField(max_length=32, blank=True, verbose_name=u'Ед. изм.y')

    class   Meta:
        verbose_name            = u'Строка медзаписи'
        verbose_name_plural     = u'Строки медзаписи'
