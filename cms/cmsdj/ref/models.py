# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

class   PMU1(models.Model):
    name    = models.CharField(max_length=255, unique=True, verbose_name=u'Наименование')

    def     __unicode__(self):
        return '%02d %s' % (self.pk, self.name)

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'ПМУ (тип)'
        verbose_name_plural     = u'ПМУ (типы)'

class   PMU2(models.Model):
    name    = models.CharField(max_length=255, unique=True, verbose_name=u'Наименование')

    def     __unicode__(self):
        return '%02d %s' % (self.pk, self.name)

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'ПМУ (класс)'
        verbose_name_plural     = u'ПМУ (классы)'

class   PMU3(models.Model):
    c1      = models.ForeignKey(PMU1, related_name='items', verbose_name=u'Тип')
    c2      = models.ForeignKey(PMU2, related_name='items', verbose_name=u'Класс')
    c3      = models.PositiveIntegerField(verbose_name=u'Код')
    name    = models.CharField(max_length=255, verbose_name=u'Наименование')

    def     __unicode__(self):
        return '%02d.%02d.%03d %s' % (self.c1.pk, self.c2.pk, self.c3, self.name)

    class   Meta:
        ordering                = ('c1', 'c2', 'c3',)
        unique_together         = ('c1', 'c2', 'c3',)
        verbose_name            = u'ПМУ'
        verbose_name_plural     = u'ПМУ'
'''
class   MKB10(models.Model):
    name    = models.CharField(max_length=128, unique=True, verbose_name=u'Наименование')

    def     __unicode__(self):
        return self.name

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Код МКБ-10'
        verbose_name_plural     = u'Коды МКБ-10'
'''
