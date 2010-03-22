# -*- coding: utf-8 -*-

from django.db import models

class	ObjectType(models.Model):
	'''
	Тип оъекта: contact, task etc
	'''
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'ID')
	name		= models.CharField(max_length=32, blank=False, unique=True, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class	Meta:
		ordering = ('name', )
		verbose_name = u'Тип объекта'
		verbose_name_plural = u'Типы объектов'

class	Object(models.Model):
	type		= models.ForeignKey(ObjectType, null=False, blank=False, unique=False, verbose_name=u'Тип')
	ancestor	= models.ForeignKey(Object, null=True,  blank=True,  unique=False, verbose_name=u'Предок')
	master		= models.ForeignKey(Object, null=True,  blank=True,  unique=False, verbose_name=u'Хозяин')
	links		= models.ManyToManyField(self, throughnull=True,  blank=True,  unique=False, verbose_name=u'Связи')

	def	__unicode__(self):
		return self.id

	class	Meta:
		ordering = ('id',)
		verbose_name = u'Объект'
		verbose_name_plural = u'Объекты'

class	ContactType(models.Model):
	'''
	Тип контакта: people/org
	'''
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'ID')
	name		= models.CharField(max_length=32, blank=False, unique=True, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class	Meta:
		ordering = ('name', )
		verbose_name = u'Тип контакта'
		verbose_name_plural = u'Типы контактов'

class	AddrShort(models.Model):
	'''
	Сокращение для адреса: ул.=улица etc
	'''
	shortname	= models.CharField(max_length=10, blank=False, unique=True, verbose_name=u'Краткое наименование')
	fullname	= models.CharField(max_length=64, blank=False, unique=True, verbose_name=u'Полное наименование')

	def	__unicode__(self):
		return self.name

	class	Meta:
		ordering = ('name', )
		verbose_name = u'Сокращение адреса'
		verbose_name_plural = u'Сокращения адресов'

class	AddrType(models.Model):
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'ID')
	name		= models.CharField(max_length=32, blank=False, unique=True, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class	Meta:
		ordering = ('name', )
		verbose_name = u'Тип адреса'
		verbose_name_plural = u'Типы адресов'

class	Contact(Object):
	contacttype	= models.ForeignKey(ContactType, null=False, blank=False, unique=False, verbose_name=u'Тип')
