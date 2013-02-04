# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from enum.models import *

# main models
class   Person(models.Model):
    lastname    = models.CharField(max_length=32, verbose_name=u'Фамилия')
    firstname   = models.CharField(max_length=32, verbose_name=u'Имя')
    midname     = models.CharField(max_length=32, blank=True, verbose_name=u'Отчество')
    gender      = models.ForeignKey(Gender, related_name='+', verbose_name=u'Пол')
    birthdate   = models.DateField(max_length=32, blank=True, null=True, verbose_name=u'Дата рождения')
    birthplace  = models.CharField(max_length=64, blank=True, verbose_name=u'Место рождения')

    def     __unicode__(self):
        return self.lastname + self.firstname

    class   Meta:
        #app_label               = 'Ядро'
        ordering                = ('lastname', 'firstname', 'midname')
        verbose_name            = u'Человек'
        verbose_name_plural     = u'Люди'

class   PersonAddress(models.Model):
    person      = models.ForeignKey(Person, related_name='Адреса', verbose_name=u'Людь')
    addrtype    = models.ForeignKey(PersonAddrType, related_name='+', verbose_name=u'Тип')
    # FK to ref.Address
    no          = models.CharField(max_length=5, verbose_name=u'Дом')
    #htype       = models.CharField(max_length=4, verbose_name=u'корп/лит')
    housing     = models.CharField(max_length=3, verbose_name=u'Корпус')
    building    = models.CharField(max_length=3, verbose_name=u'Строение')
    #atype       = models.CharField(max_length=3, verbose_name=u'кв/пом')
    app         = models.CharField(max_length=4, verbose_name=u'Квартира')

    def     __unicode__(self):
        return self.no

    class   Meta:
        unique_together         = (('person', 'addrtype',),)
        ordering                = ('person', 'no', )
        verbose_name            = u'Адрес человека'
        verbose_name_plural     = u'Адреса людей'

class   PersonPhone(models.Model):
    person      = models.ForeignKey(Person, related_name='Телефоны', verbose_name=u'Людь')
    phonetype   = models.ForeignKey(PersonPhoneType, related_name='+', verbose_name=u'Тип')
    ccode       = models.CharField(max_length=3, verbose_name=u'Код страны')
    tcode       = models.CharField(max_length=6, verbose_name=u'Код транка')
    cno         = models.CharField(max_length=7, verbose_name=u'Номер (чистый)')
    hno         = models.CharField(max_length=9, verbose_name=u'Номер (читаемый)')

    def     __unicode__(self):
        return "+%s (%s) %s" % (self.ccode, self.tcode, self.hno)

    class   Meta:
        #unique_together         = (('person', 'addrtype',),)
        ordering                = ('person', 'phonetype', 'ccode', 'tcode', 'cno')
        verbose_name            = u'Телефон'
        verbose_name_plural     = u'Телефоны'

class   PersonEmail(models.Model):
    person      = models.ForeignKey(Person, related_name='Эпочты', verbose_name=u'Людь')
    email       = models.EmailField(verbose_name=u'Мыло')

    def     __unicode__(self):
        return self.email

    class   Meta:
        unique_together         = (('person', 'email',),)
        ordering                = ('person', 'email',)
        verbose_name            = u'Эпочта'
        verbose_name_plural     = u'Эпочты'

class   PersonDocument(models.Model):
    person      = models.ForeignKey(Person, related_name='Документы', verbose_name=u'Людь')
    doctype     = models.ForeignKey(PersonDocType, related_name='+', verbose_name=u'Тип')
    series      = models.CharField(max_length=4, verbose_name=u'Серия')
    no          = models.CharField(max_length=8, verbose_name=u'Номер')
    date        = models.DateField(verbose_name=u'Дата выдачи')
    place       = models.CharField(max_length=128, blank=True, verbose_name=u'Кем выдано')
    addon       = models.CharField(max_length=32, blank=True, verbose_name=u'Дополнение')

    def     __unicode__(self):
        return '%s %s №%s' % (self.doctype.name, self.series, self.no)

    class   Meta:
        #unique_together         = (('person', 'addrtype',),)
        ordering                = ('person', 'doctype', )
        verbose_name            = u'Документ'
        verbose_name_plural     = u'Документы'

class   PersonCode(models.Model):
    person      = models.ForeignKey(Person, related_name='Коды', verbose_name=u'Людь')
    codetype    = models.ForeignKey(PersonCodeType, related_name='+', verbose_name=u'Тип')
    value       = models.CharField(max_length=32, verbose_name=u'Значение')

    def     __unicode__(self):
        return '%s %s' % (self.codetype.name, self.value)

    class   Meta:
        unique_together         = (('person', 'codetype',), ('codetype', 'value',),)
        ordering                = ('person', 'codetype', )
        verbose_name            = u'Код'
        verbose_name_plural     = u'Коды'
