# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

class   MKB10(models.Model):
    name    = models.CharField(max_length=128, unique=True, verbose_name=u'Наименование')

    def     __unicode__(self):
        return self.name

    class   Meta:
        ordering                = ('name', )
        verbose_name            = u'Код МКБ-10'
        verbose_name_plural     = u'Коды МКБ-10'
