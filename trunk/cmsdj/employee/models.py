# -*- coding: utf-8 -*-
'''
Employee
'''

from django.db import models
from django.conf import settings

from core.models import Person
from enum.models import DOW

import datetime, re

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

    def     get_name_wrapped(self):
        #print re.findall('\w+', self.name)
        #return re.findall(r"\w+", self.name)
        return self.name.replace('-', ' ').split(' ')

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
    rate        = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, verbose_name=u'Ставка')

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
    schedule    = models.ForeignKey(RoomSchedule, related_name='entries', verbose_name=u'ГК')
    room        = models.ForeignKey(Room, related_name='+', verbose_name=u'Кабинет')
    dow         = models.ForeignKey(DOW, related_name='+', verbose_name=u'День')
    specialty   = models.ForeignKey(Specialty, related_name='rsentries', verbose_name=u'Специальность')
    begtime     = models.PositiveIntegerField(verbose_name=u'с')
    endtime     = models.PositiveIntegerField(verbose_name=u'по')

    class   Meta:
        ordering                = ('schedule', 'room', 'dow', 'begtime')
        verbose_name            = u'Слот кабинета'
        verbose_name_plural     = u'Слоты кабинетов'

    def     __unicode__(self):
        return '%s, каб.№%d: %s %02d:%02d-%02d:%02d - %s' % (self.schedule, self.room.pk, self.dow, self.begtime/60, self.begtime%60, self.endtime/60, self.endtime%60, self.specialty.name)

    def     __min2str(self, m):
        return '%02d:%02d' % (m/60, m%60)

    def     get_begstr(self):
        return self.__min2str(self.begtime)

    def     get_endstr(self):
        return self.__min2str(self.endtime)

    def     __min2time(self, m):
        return datetime.time(m/60, m%60)

    def     get_begtime(self):
        return self.__min2time(self.begtime)

    def     get_endtime(self):
        return self.__min2time(self.endtime)

class   RoomScheduleEntryDoc(models.Model):
    rse         = models.ForeignKey(RoomScheduleEntry, related_name='docs', verbose_name=u'Слот')
    doc         = models.ForeignKey(Employee, related_name='+', verbose_name=u'Доктор')
    begtime     = models.PositiveIntegerField(verbose_name=u'с')
    endtime     = models.PositiveIntegerField(verbose_name=u'по')

    class   Meta:
        ordering                = ('rse', 'doc', 'begtime')
        verbose_name            = u'Слот врача'
        verbose_name_plural     = u'Слоты врачей'

    def     __unicode__(self):
        return '%s: %s' % (str(self.rse), str(self.doc))

    def     __min2str(self, m):
        return '%02d:%02d' % (m/60, m%60)

    def     get_begstr(self):
        return self.__min2str(self.rse.begtime + self.begtime)

    def     get_endstr(self):
        return self.__min2str(self.rse.begtime + self.endtime)

    def     __min2time(self, m):
        return datetime.time(m/60, m%60)

    def     get_begtime(self):
        return self.__min2time(self.rse.begtime + self.begtime)

    def     get_endtime(self):
        return self.__min2time(self.rse.begtime + self.endtime)

class   Ticket(models.Model):
    patient     = models.ForeignKey(Person, related_name='tickets', verbose_name=u'Людь')
    date        = models.DateField(verbose_name=u'Дата')
    begtime     = models.TimeField(verbose_name=u'Начало')
    endtime     = models.TimeField(verbose_name=u'Конец')
    specialty   = models.ForeignKey(Specialty, related_name='tickets', verbose_name=u'Специальность')
    rse         = models.ForeignKey(RoomScheduleEntry, null=True, blank=True, related_name='tickets', verbose_name=u'Слот')

    class   Meta:
        verbose_name            = u'Талончик'
        verbose_name_plural     = u'Талончики'
