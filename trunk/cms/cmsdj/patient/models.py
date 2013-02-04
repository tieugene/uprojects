# -*- coding: utf-8 -*-
'''
Patient
'''

from django.db import models
from django.conf import settings

from core.models import Person

class   Patient(models.Model):
    person      = models.OneToOneField(Person, verbose_name=u'Людь')

    def     __unicode__(self):
        return self.person.name

    class   Meta:
        ordering                = ('person', )
        verbose_name            = u'Поциэнт'
        verbose_name_plural     = u'Поциэнты'
