# -*- coding: utf-8 -*-
'''
Okato	ОКАТО
Okv	ОКВ	=> ISO 4217
Okved	ОКВЭД	
Okei	ОКЕИ	
Okp	ОКП	
Oksm	ОКСМ	=> ISO 3166
Okud	ОКУД
Okopf	ОКОПФ
KLADR	КЛАДР
BIK	БИК	=> ISO 9362
PhCountry		Справочник телефонных кодов стран мира
PhTrunc		Справочник телефонных кодов магистралей
ISO639	ISO 639	Коды языков
'''

import os

from django.db import models

class	KladrShort(models.Model):	# SOCRBASE
	name		= models.CharField(max_length=10, blank=False, unique=True, verbose_name=u'Наименование')		# SCNAME
	fullname	= models.CharField(max_length=29, blank=False, unique=True, verbose_name=u'Полное наименование')	# SOCRNAME

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'Сокращение'
		verbose_name_plural	= u'Сокращения'

class	KladrStateType(models.Model):
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

	def	getparents(self):
		'''
		return list of all parents
		'''
		retvalue = list()
		p = self.parent
		while (p):
			retvalue.append(p)
			p = p.parent
		retvalue.reverse()
		return retvalue

class	Okato(models.Model):
	'''
	Общероссийский классификатор объектов административно-территориального деления
	id - by OKATO
	'''
	
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=100, blank=False, unique=False, verbose_name=u'Наименование')

	def	asstr(self):
		return u'%d: %s' % (self.id, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКАТО'
		verbose_name_plural = u'Коды ОКАТО'

class	Okopf(models.Model):
	"""
	id - by OKOPF, short int
	"""
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
	shortname	= models.CharField(max_length=10, null=True, blank=True, verbose_name=u'Краткое наименование')
	namedp		= models.CharField(max_length=100, blank=True, unique=False, verbose_name=u'Наименование (д.п.)')
	disabled	= models.BooleanField(blank=False, verbose_name=u'Не выбирать')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')

	def	asstr(self):
		if (self.shortname):
			return "%s: %s" % (self.shortname, self.name)
		else:
			return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКОПФ'
		verbose_name_plural = u'Коды ОКОПФ'

class	Okved(models.Model):
	"""
	id - by OKVED, str
	"""
	id		= models.CharField(max_length=6, primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=400, blank=False, unique=False, verbose_name=u'Наименование')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')

	def	fmtid(self):
		l = len(self.id)
		if (l < 3):
			return id
		elif (l > 4):
			return u'%s.%s.%s' % (self.id[:2], self.id[2:4], self.id[4:])
		else:
			return u'%s.%s' % (self.id[:2], self.id[2:])

	def	asstr(self):
		return u'%s %s' % (self.fmtid(), self.name[:100])

	def	asshortstr(self):
		if (len(self.name) > 50):
			s = self.name[:50] + "<br/>" + self.name[50:]
		else:
			s = self.name
		return u'%s - %s' % (self.fmtid(), s)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКВЭД'
		verbose_name_plural = u'Коды ОКВЭД'

