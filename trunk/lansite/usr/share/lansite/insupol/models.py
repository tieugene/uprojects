# -*- coding: utf-8 -*-
'''
'''

from django.db import models
import os

class	Country(models.Model):
	'''
	Countries by ISO-3166-1 (http://en.wikipedia.org/wiki/ISO_3166-1). And ОКСМ.
	Todo: add flag :-)
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	a2		= models.CharField(max_length=2, null=False, blank=False, unique=True, verbose_name=u'2-симв код (en)')
	a3		= models.CharField(max_length=3, null=False, blank=False, unique=True, verbose_name=u'3-симв код (en)')
	name_en		= models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name=u'Наименование (en)')
	name_ru		= models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name=u'Наименование (ru)')
	_xmlname	= u'country'

	def	asstr(self):
		return self.name_ru

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name_ru',)
		verbose_name = u'Страна'
		verbose_name_plural = u'Страны'

class	Currency(models.Model):
	'''
	ISO 4217
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(null=False, blank=False, unique=True, max_length=3, verbose_name=u'Наименование')
	_xmlname	= u'currency'

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'Валюта'
		verbose_name_plural = u'Валюты'

class	Program(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(null=False, blank=False, unique=True, max_length=1, verbose_name=u'Наименование')
	_xmlname	= u'program'

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'Программа'
		verbose_name_plural = u'Программы'

class	Ratio(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField		(null=False, blank=False, unique=True, max_length=2, verbose_name=u'Наименование')
	value		= models.DecimalField		(null=True, blank=True, max_digits=3, decimal_places=2, verbose_name=u'Значение')
	parent		= models.ForeignKey		('self', null=True, blank=True, verbose_name=u'Группа')
	personal	= models.BooleanField		(null=False, blank=False, verbose_name=u'И для застрахованного')
	comments	= models.CharField		(null=False, blank=False, unique=True, max_length=100, verbose_name=u'Коментарий')
	_xmlname	= u'ratio'

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'Коэффициент'
		verbose_name_plural = u'Коэффициенты'

class	State(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(null=False, blank=False, unique=True, max_length=1, verbose_name=u'Наименование')
	_xmlname	= u'state'

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'Состояние'
		verbose_name_plural = u'Состояния'

class	SumPer(models.Model):
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Сумма')
	_xmlname	= u'sumper'

	def	asstr(self):
		return str(self.id)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'Страховая сумма'
		verbose_name_plural = u'Страховые суммы'

class	Policy(models.Model):
	'''
	Policies
	'''
	id		= models.PositiveIntegerField	(primary_key=True, verbose_name=u'Серия-Номер')
	date		= models.DateField		(null=False, blank=False, verbose_name=u'Дата')
	program		= models.ForeignKey		(Program, null=False, blank=False, verbose_name=u'Программа')
	isorg		= models.BooleanField		(null=False, blank=False, verbose_name=u'Юрлицо')
	insurant	= models.CharField		(null=False, blank=False, max_length=100, verbose_name=u'Страхователь')
	datebirth	= models.DateField		(null=True,  blank=True,  verbose_name=u'Дата рождения')
	address		= models.CharField		(null=False, blank=False, max_length=100, verbose_name=u'Адрес')
	phone		= models.CharField		(null=False, blank=False, max_length=50, verbose_name=u'Телефон')
	dateeff		= models.DateField		(null=False, blank=False, verbose_name=u'Дата начала')		# Date effective
	dateexp		= models.DateField		(null=False, blank=False, verbose_name=u'Дата окончания')	# Date expired
	days		= models.PositiveIntegerField	(null=False, blank=False, verbose_name=u'Дней')
	sumper		= models.ForeignKey		(SumPer, null=False, blank=False, verbose_name=u'Страховая сумма')
	currency	= models.ForeignKey		(Currency, null=False, blank=False, verbose_name=u'Валюта')
	course		= models.DecimalField		(null=False, blank=False, max_digits=7, decimal_places=4, verbose_name=u'Курс')
	fixrate		= models.BooleanField		(null=False, blank=False, verbose_name=u'Фиксированный тариф')
	rate		= models.DecimalField		(null=False, blank=False, max_digits=5, decimal_places=2, verbose_name=u'Тариф')
	refusal		= models.DecimalField		(null=True, blank=True, max_digits=5, decimal_places=2, verbose_name=u'Отказ')
	freeratio	= models.DecimalField		(null=True, blank=True, max_digits=3, decimal_places=2, verbose_name=u'Общие свободный коэффициент')
	terms		= models.CharField		(null=True, blank=True, max_length=100, verbose_name=u'Особые условия')
	issuedate	= models.DateField		(null=False, blank=False, verbose_name=u'Дата выдачи')
	issueplace	= models.CharField		(null=False, blank=False, max_length=100, verbose_name=u'Место выдачи')
	contractno	= models.PositiveIntegerField	(null=True, blank=True, verbose_name=u'Номер договора')
	contractdate	= models.DateField		(null=True, blank=True, verbose_name=u'Дата договора')
	attorneyno	= models.PositiveIntegerField	(null=True, blank=True, verbose_name=u'Номер доверенности')
	attorneydate	= models.DateField		(null=True, blank=True, verbose_name=u'Дата доверенности')
	premium		= models.DecimalField		(null=False, blank=False, max_digits=5, decimal_places=2, verbose_name=u'Общая страховая премия')
	reward		= models.DecimalField		(null=False, blank=False, max_digits=5, decimal_places=2, verbose_name=u'КВ')
#	user		= models.ForeignKey		(User, null=False, blank=False, verbose_name=u'Пользователь')
	state		= models.ForeignKey		(State, null=False, blank=False, verbose_name=u'Состояние')
	territory	= models.ManyToManyField	(Country, through='PolicyCountry', verbose_name=u'Территория')
	ratios		= models.ManyToManyField	(Ratio, through='PolicyRatio', verbose_name=u'Общие коэффициенты')
	_xmlname	= u'policy'

	def	asstr(self):
		return u'%d' % (self.id,)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'Полис'
		verbose_name_plural = u'Полисы'

class	PolicyCountry(models.Model):
	policy		= models.ForeignKey	(Policy, verbose_name=u'Полис')
	country		= models.ForeignKey	(Country, verbose_name=u'Страна')
	_xmlname	= u'policycountry'

	def	asstr(self):
		return u'%s: %s' % (self.policy.asstr(), self.country.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('policy', 'country')
		verbose_name = u'Полис.Страна'
		verbose_name_plural = u'Полис.Страны'

class	PolicyRatio(models.Model):
	policy		= models.ForeignKey	(Policy, verbose_name=u'Полис')
	ratio		= models.ForeignKey	(Ratio, verbose_name=u'Коэффициент')
	_xmlname	= u'policycountry'

	def	asstr(self):
		return u'%s: %s' % (self.policy.asstr(), self.ratio.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('policy', 'ratio')
		verbose_name = u'Полис.Коэффициент'
		verbose_name_plural = u'Полис.Коэффициенты'

class	Insured(models.Model):
	policy		= models.ForeignKey			(Policy, verbose_name=u'Полис')
	orderno		= models.PositiveSmallIntegerField	(null=False, blank=False, verbose_name=u'№ пп')
	lastname	= models.CharField			(null=False, blank=False, max_length='32', verbose_name=u'Фамилия')
	firstname	= models.CharField			(null=False, blank=False, max_length='32', verbose_name=u'Имя')
	datebirth	= models.DateField			(null=False, blank=False, verbose_name=u'Дата рождения')
	address		= models.CharField			(null=False, blank=False, max_length=100, verbose_name=u'Адрес')
	freeratio	= models.DecimalField			(null=True,  blank=True,  max_digits=3, decimal_places=2, verbose_name=u'Свободный коэффициент')
	_xmlname	= u'insured'

	def	asstr(self):
		return u'%s: %s %s' % (self.policy.asstr(), self.lastname, self.firstname)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('policy', 'orderno')
		verbose_name = u'Полис.Коэффициент'
		verbose_name_plural = u'Полис.Коэффициенты'

#class	InsuredRatio(models.Model):
#	pass

modellist	= (Country, Currency, Program, Ratio, State, SumPer, Policy, PolicyCountry, PolicyRatio, Insured)
