# -*- coding: utf-8 -*-
'''
Enum
'''

from django.db import models
from django.conf import settings

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class   Gender(models.Model):
    '''man, woman'''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=3, unique=True)

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Пол'
        verbose_name_plural     = u'Полы'

    def     __unicode__(self):
        return self.name

class   DOW(models.Model):
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=3, unique=True)
    longname    = models.CharField(max_length=12, unique=True)

    class   Meta:
        ordering                = ('id', )
        verbose_name            = u'День недели'
        verbose_name_plural     = u'Дни недели'

    def     __unicode__(self):
        return self.name

class   PersonAddrType(models.Model):
    '''
    * домашний
    * почтовый
    * проживания
    * пребывания
    * регистрации
    '''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=16, unique=True)

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Тип адреса'
        verbose_name_plural     = u'Типы адресов'

    def     __unicode__(self):
        return self.name

class   PersonPhoneType(models.Model):
    '''мобильный (Cell), домашний (Телефонная сеть общего пользования, ТСОП, ТфОП (англ. PSTN, Public Switched Telephone Network))'''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=16, unique=True)

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Тип телефона'
        verbose_name_plural     = u'Типы телефонов'

    def     __unicode__(self):
        return self.name

class   PersonDocType(models.Model):
    '''
    Паспорт гражданина РФ
    Вид на жительство
    Иностранный паспорт
    Водительское удостоверение
    '''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=32, unique=True)

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Тип документа'
        verbose_name_plural     = u'Типы документов'

    def     __unicode__(self):
        return self.name

class   PersonCodeType(models.Model):
    '''МНН, СНИЛС, ЕНП'''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=16, unique=True)

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Тип кода'
        verbose_name_plural     = u'Типы кодов'

    def     __unicode__(self):
        return self.name

# htype
# apptype
