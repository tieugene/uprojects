# -*- coding: utf-8 -*-
'''
SRO2

models: 32
'''

import os

from django.db import models
from xdg import Mime

class	Insurer(models.Model):
	name		= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
	fullname	= models.CharField(max_length=100, blank=True, unique=False, verbose_name=u'Полное наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'Страховщик'
		verbose_name_plural = u'Страховщики'

class	Okato(models.Model):
	'''
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
	'''
	id - by OKOPF, short int
	'''
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
	'''
	id - by OKVED, str
	'''
	id		= models.CharField(max_length=6, primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=255, blank=False, unique=False, verbose_name=u'Наименование')
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

class	SroType(models.Model):
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'Тип СРО'
		verbose_name_plural = u'Типы СРО'

class	Sro(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')
	fullname	= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Полное наименование')
	regno		= models.CharField(max_length=20, blank=False, unique=True, verbose_name=u'Рег. №')
	type		= models.ForeignKey(SroType, blank=False, verbose_name=u'Тип')
	own		= models.BooleanField(blank=False, default=False, verbose_name=u'Своё')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'СРО'
		verbose_name_plural = u'СРО'

class	Stage(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	srotype		= models.ForeignKey(SroType, blank=False, verbose_name=u'Тип СРО')
	name		= models.CharField(max_length=255, blank=False, unique=True, verbose_name=u'Наименование')
	hq		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Кол-во ВО', help_text=u'Количество специалистов с высшим образованием')
	hs		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Стаж ВО', help_text=u'Минимальный стаж специалистов с высшим образованием')
	mq		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Кол-во СО', help_text=u'Количество специалистов со средним образованием')
	ms		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Стаж СО', help_text=u'Минимальный стаж специалистов со средним образованием')

	def	asstr(self):
		return u'%02d %s' % (self.id, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'Вид работ'
		verbose_name_plural = u'Виды работ'

class	Job(models.Model):
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Код')
	stage		= models.ForeignKey(Stage, verbose_name=u'Группа работ')
	okdp		= models.PositiveIntegerField(null=False, verbose_name=u'ОКДП')
	name		= models.CharField(max_length=255, blank=False, verbose_name=u'Наименование')

	def	asstr(self):
		return u'%02d: %d' % (self.stage.id, self.okdp)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering	= ('id',)
		verbose_name = u'Работа'
		verbose_name_plural = u'Работы'

class	Speciality(models.Model):
	name		= models.CharField(max_length=255, blank=False, unique=True, verbose_name=u'Наименование')
	stages		= models.ManyToManyField(Stage, through='SpecialityStage', verbose_name=u'Виды работ')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering	= ('name',)
		verbose_name	= u'Специальность'
		verbose_name_plural = u'Специальности'

class	SpecialityStage(models.Model):
	speciality	= models.ForeignKey(Speciality, verbose_name=u'Специальность')
	stage		= models.ForeignKey(Stage, verbose_name=u'Вид работ')

	def	asstr(self):
		return u'%s:%s' % (self.speciality, self.stage)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Специальность.ВидРабот'
		verbose_name_plural	= u'Специальности.ВидыРабот'
		unique_together		= (('speciality', 'stage',),)

class	Skill(models.Model):
	name		= models.CharField(max_length=50, blank=False, unique=True, verbose_name=u'Наименование')
	high		= models.BooleanField(blank=False, null=False, default=False, verbose_name=u'Высшее')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'Квалификация'
		verbose_name_plural = u'Квалификации'

class	EventType(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name = u'Тип события'
		verbose_name_plural = u'Типы событий'

class	Role(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')

	def	asstr(self):
		retvalue = self.name
		if self.comments:
			retvalue += u' (%s)' % self.comments
		return retvalue

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'Должность'
		verbose_name_plural = u'Должности'

class	Person(models.Model):
	firstname	= models.CharField(max_length=16, blank=False, verbose_name=u'Имя')
	midname		= models.CharField(max_length=24, blank=True, verbose_name=u'Отчество')
	lastname	= models.CharField(max_length=24, blank=False, verbose_name=u'Фамилия')
	skills		= models.ManyToManyField(Skill, through='PersonSkill', verbose_name=u'Квалификации')
	phone		= models.CharField(null=True, blank=True, max_length=25, verbose_name=u'Телефон')

	def	asstr(self):
		return u'%s %s %s' % (self.lastname, self.firstname, self.midname)

	def	getfio(self):
		return u'%s %s. %s.' % (self.lastname, self.firstname[:1], self.midname[:1])

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('lastname', 'firstname', 'midname')
		verbose_name = u'Человек'
		verbose_name_plural = u'Люди'

class	PersonSkill(models.Model):
	person		= models.ForeignKey(Person, verbose_name=u'Человек')
	speciality	= models.ForeignKey(Speciality, verbose_name=u'Специальность')
	skill		= models.ForeignKey(Skill, verbose_name=u'Квалификация')
	year		= models.PositiveIntegerField(null=False, blank=False, verbose_name=u'Год')
	skilldate	= models.DateField(null=True, blank=True, verbose_name=u'Дата окончания')
	school		= models.CharField(max_length=100, null=False, blank=False, verbose_name=u'Учебное заведение')
	seniority	= models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Стаж')
	seniodate	= models.DateField(null=True, blank=True, verbose_name=u'Дата актуальности стажа')
	tested		= models.DateField(null=True, blank=True, verbose_name=u'Дата последней аттестации')
	courseno	= models.CharField(max_length=50, null=True, blank=True, verbose_name=u'СоПК.№')
	coursedate	= models.DateField(null=True, blank=True, verbose_name=u'СоПК.Дата Выдачи')
	coursename	= models.CharField(max_length=50, null=True, blank=True, verbose_name=u'СоПК.Наименование курсов')
	courseschool	= models.CharField(max_length=100, null=True, blank=True, verbose_name=u'СоПК.УЗ')

	def	asstr(self):
		return u'%s: %s, %s' % (self.person.asstr(), self.speciality.asstr(), self.skill.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name = u'Человек.Квалификация'
		verbose_name_plural = u'Человек.Квалификации'

class	Org(models.Model):
	name		= models.CharField(null=False, blank=False, max_length=40, unique=False, verbose_name=u'Наименование')
	fullname	= models.CharField(null=False, blank=False, max_length=100, unique=False, verbose_name=u'Полное наименование')
	okopf		= models.ForeignKey(Okopf, null=False, blank=False, verbose_name=u'ОКОПФ')
	egruldate	= models.DateField(null=True, blank=True, verbose_name=u'Дата регистрации в ЕГРЮЛ')
	inn		= models.PositiveIntegerField(null=False, blank=False, unique=True, verbose_name=u'ИНН')
	kpp		= models.PositiveIntegerField(null=True, blank=True, verbose_name=u'КПП')
	ogrn		= models.PositiveIntegerField(null=False, blank=False, unique=True, verbose_name=u'ОГРН')
	okato		= models.ForeignKey(Okato, null=True, blank=True, verbose_name=u'ОКАТО')
	laddress	= models.CharField(null=False, blank=False, max_length=255, verbose_name=u'Адрес юридический')
	raddress	= models.CharField(null=True, blank=True, max_length=255, verbose_name=u'Адрес почтовый')
	comments	= models.TextField(null=True, blank=True, verbose_name=u'Коментарии')
	okveds		= models.ManyToManyField(Okved, through='OrgOkved', verbose_name=u'Коды ОКВЭД')
	stuffs		= models.ManyToManyField(Person, through='OrgStuff', verbose_name=u'Штат')
	sro		= models.ManyToManyField(Sro, through='OrgSro', verbose_name=u'СРО')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name		= u'Организация'
		verbose_name_plural	= u'Организации'

class	OrgOkved(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	okved		= models.ForeignKey(Okved, verbose_name=u'ОКВЭД')

	def	asstr(self):
		return self.okved.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.ОКВЭД'
		verbose_name_plural	= u'Организация.Коды ОКВЭД'
		unique_together		= [('org', 'okved')]

class	OrgPhone(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	phone		= models.CharField(null=False, blank=False, max_length=25, verbose_name=u'Номер')

	def	asstr(self):
		return self.phone

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'Телефон'
		verbose_name_plural	= u'Телефоны'

class	OrgEmail(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	URL		= models.EmailField(null=False, blank=False, unique=False, verbose_name=u'Ссылка')

	def	asstr(self):
		return self.URL

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('URL',)
		verbose_name = u'Электропочта'
		verbose_name_plural = u'Адреса электропочты'
		unique_together		= [('org', 'URL')]

class	OrgWWW(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	URL		= models.URLField(blank=False, unique=True, verbose_name=u'Ссылка')

	def	asstr(self):
		return self.URL

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('URL',)
		verbose_name = u'WWW'
		verbose_name_plural = u'WWW'
		unique_together		= [('org', 'URL')]

class	OrgStuff(models.Model):
	'''
	FIXME: permanent => Fulltime job
	'''
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	role		= models.ForeignKey(Role, verbose_name=u'Должность')
	person		= models.ForeignKey(Person, verbose_name=u'Человек')
	leader		= models.BooleanField(default=Fasle, verbose_name=u'Руководитель')
	permanent	= models.BooleanField(default=Fasle, verbose_name=u'Основное')

	def	asstr(self):
		return u'%s: %s' % (self.role.asstr(), self.person.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Должностное лицо'
		verbose_name_plural	= u'Организация.Должностные лица'
		unique_together		= [('org', 'role', 'person')]

class	OrgSro(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	sro		= models.ForeignKey(Sro, verbose_name=u'СРО')
	regno		= models.PositiveIntegerField(null=True, blank=True, unique=True, verbose_name=u'Реестровый №')
	regdate		= models.DateField(null=True, blank=True, verbose_name=u'Дата членства в НП')
	paydate		= models.DateField(null=True, blank=True, verbose_name=u'Дата оплаты взноса в КФ')
	paysum		= models.PositiveIntegerField(null=True, blank=False, verbose_name=u'Сумма взноса в КФ')
	paydatevv	= models.DateField(null=True, blank=True, verbose_name=u'Дата оплаты вступительного взноса')
	comments	= models.TextField(null=True, blank=True, verbose_name=u'Коментарии')
	publish		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Публиковать')
	events		= models.ManyToManyField(EventType, through='OrgEvent', verbose_name=u'События')

	def	asstr(self):
		return u'%s: %s' % (self.org.name, )

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name		= u'Организация.СРО'
		verbose_name_plural	= u'Организации.СРО'

class	OrgEvent(models.Model):
	orgsro		= models.ForeignKey(OrgSro, verbose_name=u'Организация.СРО')
	type		= models.ForeignKey(EventType, verbose_name=u'Типа события')
	date		= models.DateField(blank=False, verbose_name=u'Дата')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарий')

	def	asstr(self):
		return self.type.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('orgsro', 'date')
		verbose_name		= u'Организация.СРО.Событие'
		verbose_name_plural	= u'Организация.СРО.События'

class	OrgLicense(models.Model):
	orgsro		= models.OneToOneField(OrgSro, verbose_name=u'Организация.СРО')
	no		= models.CharField(null=False, blank=False, max_length=100, unique=True, verbose_name=u'Номер лицензии')
	datefrom	= models.DateField(null=False, blank=False, verbose_name=u'Выдана')
	datedue		= models.DateField(null=False, blank=False, verbose_name=u'Действительна до')

	def	asstr(self):
		return u'%s, до %s' % (self.no, self.datedue)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('orgsro',)
		verbose_name = u'Организация.СРО.Лицензия'
		verbose_name_plural = u'Организация.СРО.Лицензии'

class	OrgInsurance(models.Model):
	orgsro		= models.OneToOneField(Org, verbose_name=u'Организация.СРО')
	insurer		= models.ForeignKey(Insurer, null=True, blank=True, verbose_name=u'Страховщик')
	no		= models.CharField(null=False, blank=False, unique=True, max_length=50, verbose_name=u'Номер договора')
	date		= models.DateField(null=False, blank=False, verbose_name=u'Дата договора')
	sum		= models.PositiveIntegerField(null=False, blank=False, verbose_name=u'Страховая сумма')
	datefrom	= models.DateField(null=True, blank=True, verbose_name=u'Страховка с')
	datedue		= models.DateField(null=True, blank=True, verbose_name=u'Страховка до')

	def	asstr(self):
		return u'%s от %s, %d руб, с %s по %s' % (self.no, self.date, self.sum, self.datefrom, self.datedue)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('orgsro',)
		verbose_name = u'Организация.Страховка'
		verbose_name_plural = u'Организация.Страховки'

class	Protocol(models.Model):
	sro		= models.OneToOneField(Sro, verbose_name=u'СРО')
	no		= models.PositiveIntegerField(null=False, blank=False, unique=False, verbose_name=u'№')
	date		= models.DateField(null=False, blank=False, verbose_name=u'Дата')

	def	asstr(self):
		return u'№ %d от %s' % (self.no, self.date)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('date',)
		verbose_name		= u'Протокол'
		verbose_name_plural	= u'Протоколы'

class	StageListType(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=30, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return u'%d: %s' % (self.id, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'ТипСпискаВидовРабот'
		verbose_name_plural	= u'ТипыСпискаВидовРабот'

class	StageList(models.Model):
	orgsro		= models.ForeignKey(OrgSro, verbose_name=u'Организация.СРО')
	type		= models.ForeignKey(StageListType, verbose_name=u'Тип')
	stages		= models.ManyToManyField(Stage, through='PermitStage', verbose_name=u'Виды работ')

	def	asstr(self):
		return u'%s: %s' % (self.orgsro.asstr(), self.type.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'СписокВидовРабот'
		verbose_name_plural	= u'СпискиВидовРабот'

class	PermitStage(models.Model):
	stagelist	= models.ForeignKey(StageList, verbose_name=u'Список')
	stage		= models.ForeignKey(Stage, verbose_name=u'Вид работ')
	jobs		= models.ManyToManyField(Job, through='PermitStageJob', verbose_name=u'Работы')

	def	asstr(self):
		return u'%s: %s' % (self.stagelist.asstr(), self.stage.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'СписокВидовРабот.ВидРабот'
		verbose_name_plural	= u'СписокВидовРабот.ВидыРабот'
		unique_together		= [('stagelist', 'stage')]

class	PermitStageJob(models.Model):
	permitstage	= models.ForeignKey(PermitStage, verbose_name=u'Разрешение.Вид работ')
	job		= models.ForeignKey(Job, verbose_name=u'Работа')	#, limit_choices_to = { 'permit_stage__eq': self.permitstage.stage })

	def	asstr(self):
		return u'%s: %s' % (self.permitstage.asstr(), self.job.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'СписокВидовРабот.ВидРабот.Работа'
		verbose_name_plural	= u'СписокВидовРабот.ВидРабот.Работы'
		unique_together		= [('permitstage', 'job')]

class	Statement(models.Model):
	stagelist	= models.OneToOneField(StageList, verbose_name=u'СписокВидовРабот')
	date		= models.DateField(null=True, blank=True, verbose_name=u'Дата')

	def	asstr(self):
		return u'%s: %s от %s' % (self.stagelist.orgsro.asstr(), self.stagelist.type.name, self.date)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Заявление'
		verbose_name_plural	= u'Заявления'

class	Permit(models.Model):
	stagelist	= models.OneToOneField(StageList, verbose_name=u'СписокВидовРабот')
	no		= models.CharField(max_length=50, null=False, blank=False, unique=False, verbose_name=u'Рег. №')
	date		= models.DateField(null=True, blank=True, verbose_name=u'Дата')
	datedue		= models.DateField(null=True, blank=True, verbose_name=u'Дата аннулирования')
	protocol	= models.ForeignKey(Protocol, null=True, blank=True, verbose_name=u'Заседание')

	def	asstr(self):
		return u'%s: %s № %d от %s' % (self.permit.org.name, self.permit.permittype.name, self.regno, self.date)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Свидетельство'
		verbose_name_plural	= u'Свидетельства'

modellist = (
	Insurer, Okato, Okopf, Okved, SroType, Sro, Stage, Job, Speciality, SpecialityStage,
	Skill, EventType, Role, Person, PersonSkill, Org, OrgOkved, OrgPhone, OrgEmail, OrgWWW,
	OrgStuff, OrgSro, OrgEvent, OrgLicense, OrgInsurance, Protocol, StageListType, StageList, PermitStage, PermitStageJob,
	Statement, Permit
)
