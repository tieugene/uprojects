# -*- coding: utf-8 -*-
'''
Employee
'''

from django.db import models
from django.conf import settings

from core.models import Person
from enum.models import DOW

import datetime

class   Department(models.Model):
    name    = models.CharField(max_length=255, unique=True, verbose_name=u'Наименование')

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Отделение'
        verbose_name_plural     = u'Отделения'

    def     __unicode__(self):
        return self.name

class   Room(models.Model):
    '''
	14, 05 - педиатрия
	4,20,21 - терапия
	11,15,16 - стоматология
	24,29,36,37 - косметология
    '''
    id      	= models.PositiveIntegerField(primary_key=True, verbose_name=u'Номер')
    department	= models.ForeignKey(Department, related_name='rooms', verbose_name=u'Отделение')

    class   Meta:
        ordering                = ('id', )
        verbose_name            = u'Кабинет'
        verbose_name_plural     = u'Кабинеты'

    def     __unicode__(self):
        return '%02d' % self.id

class   Specialty(models.Model):
    name    = models.CharField(max_length=255, unique=True, verbose_name=u'Наименование')
    department	= models.ForeignKey(Department, related_name='specialties', verbose_name=u'Отделение')
    timeout = models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Прием, мин.')

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Специальность'
        verbose_name_plural     = u'Специальности'

    def     __unicode__(self):
        return self.name

class   Employee(models.Model):
    person      = models.OneToOneField(Person, verbose_name=u'Людь')
    specialty	= models.ManyToManyField(Specialty, through='EmployeeSpecialty')

    class   Meta:
        ordering                = ('person', )
        verbose_name            = u'Сотрудник'
        verbose_name_plural     = u'Сотрудники'

    def     __unicode__(self):
        return str(self.person)

class   EmployeeSpecialty(models.Model):
    employee	= models.ForeignKey(Employee, related_name='specialties', verbose_name=u'Врач')
    specialty	= models.ForeignKey(Specialty, related_name='employees', verbose_name=u'Специальность')
    rate      	= models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, verbose_name=u'Ставка')

    class   Meta:
        ordering                = ('employee', 'specialty')
        unique_together         = (('employee', 'specialty'),)
        verbose_name            = u'Должность сотрудника'
        verbose_name_plural     = u'Должности сотрудников'

    def     __unicode__(self):
        return '%s (%s)' % (self.specialty, self.employee)

class   StaffList(models.Model):
    begdate   = models.DateField(unique=True, default=datetime.datetime.today(), verbose_name=u'Действительно с')

    class   Meta:
        ordering                = ('begdate', )
        verbose_name            = u'Штатное расписание'
        verbose_name_plural     = u'Штатные расписания'

    def     __unicode__(self):
        return str(self.begdate)

class   StaffListEntry(models.Model):
    stafflist	= models.ForeignKey(StaffList, related_name='staves', verbose_name=u'ШР')
    specialty	= models.ForeignKey(Specialty, related_name='+', verbose_name=u'Специальность')
    qty     	= models.DecimalField(max_digits=5, decimal_places=2, verbose_name=u'Ставок')

    class   Meta:
        ordering                = ('stafflist', 'specialty')
        unique_together         = (('stafflist', 'specialty'),)
        verbose_name            = u'Штатное расписание'
        verbose_name_plural     = u'Штатные расписания'

    def     __unicode__(self):
        return '%s: %s - %d' % (self.stafflist, self.specialty, self.qty)

class   RoomSchedule(models.Model):
    begdate   = models.DateField(unique=True, default=datetime.datetime.today(), verbose_name=u'Действительно с')

    class   Meta:
        ordering                = ('begdate', )
        verbose_name            = u'График кабинетов'
        verbose_name_plural     = u'Графики кабинетов'

    def     __unicode__(self):
        return str(self.begdate)

class   RoomScheduleEntry(models.Model):
    schedule	= models.ForeignKey(RoomSchedule, related_name='staves', verbose_name=u'ШР')
    room	    = models.ForeignKey(Room, related_name='+', verbose_name=u'Кабинет')
    specialty	= models.ForeignKey(Specialty, related_name='+', verbose_name=u'Специальность')
    dow 	    = models.ForeignKey(DOW, related_name='+', verbose_name=u'День')
    begtime    	= models.PositiveIntegerField(verbose_name=u'с')
    endtime    	= models.PositiveIntegerField(verbose_name=u'по')

    class   Meta:
        ordering                = ('schedule', 'room', 'dow', 'begtime')
        #unique_together         = (('schedule', 'room'),)
        verbose_name            = u'Сокет кабинета'
        verbose_name_plural     = u'Сокеты кабинетов'

    def     __unicode__(self):
        return '%s, каб.№%d: %s %02d:%02d-%02d:%02d - %s' % (self.schedule, self.room.pk, self.dow, self.begtime/60, self.begtime%60, self.endtime/60, self.endtime%60, self.specialty.name)