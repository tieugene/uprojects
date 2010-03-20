# -*- coding: utf-8 -*-
'''
KLADR

ALTNAMES	-	6870
DOMA		-	81472
FLAT		-	0
KLADR		+	191640
SOCRBASE	+	146
STREET		+	821647
'''

import os

from django.db import models

class	Short(models.Model):	# SOCRBASE
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')				# KOD_T_ST
	name		= models.CharField(max_length=10, blank=False, unique=False, verbose_name=u'Наименование')		# SCNAME
	fullname	= models.CharField(max_length=29, blank=False, unique=False, verbose_name=u'Полное наименование')	# SOCRNAME
	level		= models.PositiveSmallIntegerField(blank=False, verbose_name=u'Уровень')				# LEVEL

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'Сокращение'
		verbose_name_plural	= u'Сокращения'

class	StateType(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	comments	= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Каменты')

	def	asstr(self):
		return self.id

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'Статус'
		verbose_name_plural	= u'Статусы'

class	Kladr(models.Model):	# KLADR+STREET
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Код')					# CODE
	parent		= models.ForeignKey('self', null=True, blank=True, verbose_name=u'Папа')
	name		= models.CharField(max_length=40, null=False, blank=False, unique=False, verbose_name=u'Наименование')	# NAME
	short		= models.ForeignKey(Short, null=True, blank=True, verbose_name=u'Сокращение')				# SOCR
	level		= models.PositiveSmallIntegerField(blank=False, verbose_name=u'Уровень')
	zip		= models.CharField(max_length=6, null=True, blank=True, unique=False, verbose_name=u'Индекс')		# INDEX
	okato		= models.CharField(max_length=11, null=True, blank=True, unique=False, verbose_name=u'ОКАТО')		# OCATD
	center		= models.ForeignKey(StateType, null=True, blank=True, unique=False, verbose_name=u'Центр')		# STATUS

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'КЛАДР'
		verbose_name_plural	= u'КЛАДРы'
