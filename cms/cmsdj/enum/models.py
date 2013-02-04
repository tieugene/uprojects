# -*- coding: utf-8 -*-
'''
Enum
'''

from django.db import models
from django.conf import settings

class   Gender(models.Model):
    '''man, woman'''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=3, unique=True)

    def     __unicode__(self):
        return self.name

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Пол'
        verbose_name_plural     = u'Полы'

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

    def     __unicode__(self):
        return self.name

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Тип адреса'
        verbose_name_plural     = u'Типы адресов'

class   PersonPhoneType(models.Model):
    '''мобильный (Cell), домашний (Телефонная сеть общего пользования, ТСОП, ТфОП (англ. PSTN, Public Switched Telephone Network))'''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=16, unique=True)

    def     __unicode__(self):
        return self.name

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Тип телефона'
        verbose_name_plural     = u'Типы телефонов'

class   PersonDocType(models.Model):
    '''
    Паспорт гражданина РФ
    Вид на жительство
    Иностранный паспорт
    Водительское удостоверение
    '''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=32, unique=True)

    def     __unicode__(self):
        return self.name

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Тип документа'
        verbose_name_plural     = u'Типы документов'

class   PersonCodeType(models.Model):
    '''МНН, СНИЛС, ЕНП'''
    id      = models.PositiveIntegerField(primary_key=True)
    name    = models.CharField(max_length=16, unique=True)

    def     __unicode__(self):
        return self.name

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Тип кода'
        verbose_name_plural     = u'Типы кодов'

# htype
# apptype
