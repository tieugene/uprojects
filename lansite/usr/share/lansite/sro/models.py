# -*- coding: utf-8 -*-
'''
models: 30 (w/o country & trunk)
'''

import os

from django.db import models
from xdg import Mime

from rfm import RenameFilesModel
#from cbm2m import CheckBoxManyToMany

def	my_upload_to(instance, filename):
	"""Generates upload path for FileField"""
	instance.name = filename
	return u'temp/%s' % filename

class	Insurer(models.Model):
	name		= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
	fullname	= models.CharField(max_length=100, blank=True, unique=False, verbose_name=u'Полное наименование')
	_xmlname	= u'insurer'

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('name',)
		verbose_name = u'Страховщик'
		verbose_name_plural = u'Страховщики'

	def	exml(self):
		retvalue = u'\t<%s id="%d" name="%s"/>\n' % (self._xmlname, self.id, self.name)

	def	ixml(self, s):
		return self

class	Okato(models.Model):
	'''
	id - by OKATO
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=100, blank=False, unique=False, verbose_name=u'Наименование')
	_xmlname	= u'okato'

	def	asstr(self):
		return u'%d: %s' % (self.id, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКАТО'
		verbose_name_plural = u'Коды ОКАТО'

	def	exml(self):
		retvalue = u'\t<%s id="%d" name="%s"/>\n' % (self._xmlname, self.id, self.name)

	def	ixml(self, s):
		return self

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
	_xmlname	= u'okopf'
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
	def	exml(self):
		retvalue = u'\t<%s id="%d" name="%s"' % (self._xmlname, self.id, self.name)
		if (self.shortname):
			retvalue += u' shortname="%s"' % self.shortname
		if (self.disabled):
			retvalue += u' disabled="1"'
		if (self.parent):
			retvalue += u' parent="%d"' % self.parent
		return retvalue + u'/>\n'
	def	ixml(self, s):
		return self

class	Okved(models.Model):
	'''
	id - by OKVED, str
	'''
	id		= models.CharField(max_length=6, primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=255, blank=False, unique=False, verbose_name=u'Наименование')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')
	_xmlname	= u'okved'
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
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКВЭД'
		verbose_name_plural = u'Коды ОКВЭД'
	def	exml(self):
		retvalue = u'\t<%s id="%s" name="%s"' % (self._xmlname, self.id, self.name)
		if (self.disabled):
			retvalue += u' disabled="1"'
		if (self.parent):
			retvalue += u' parent="%d"' % self.parent
		return retvalue + u'/>\n'
	def	asshortstr(self):
		if (len(self.name) > 50):
			s = self.name[:50] + "<br/>" + self.name[50:]
		else:
			s = self.name
		return u'%s - %s' % (self.fmtid(), s)

class	Stage(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=255, blank=False, unique=True, verbose_name=u'Наименование')
	hq		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Кол-во ВО', help_text=u'Количество специалистов с высшим образованием')
	hs		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Стаж ВО', help_text=u'Минимальный стаж специалистов с высшим образованием')
	mq		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Кол-во СО', help_text=u'Количество специалистов со средним образованием')
	ms		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Стаж СО', help_text=u'Минимальный стаж специалистов со средним образованием')
	_xmlname	= u'stage'
	def	asstr(self):
		return u'%02d %s' % (self.id, self.name)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('id',)
		verbose_name = u'Вид работ'
		verbose_name_plural = u'Виды работ'
	def	exml(self):
		retvalue = u'\t<%s id="%d" name="%s"' % (self._xmlname, self.id, self.name)
		if (self.hq):
			retvalue += u' hq="%d"' % self.hq
		if (self.hs):
			retvalue += u' hs="%d"' % self.hs
		if (self.mq):
			retvalue += u' mq="%d"' % self.mq
		if (self.ms):
			retvalue += u' ms="%d"' % self.ms
		return retvalue + u'/>\n'

class	Job(models.Model):
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Код')
	stage		= models.ForeignKey(Stage, verbose_name=u'Группа работ')
	okdp		= models.PositiveIntegerField(null=False, verbose_name=u'ОКДП')
	name		= models.CharField(max_length=255, blank=False, verbose_name=u'Наименование')
	_xmlname	= u'job'
	def	asstr(self):
		return u'%02d: %d' % (self.stage.id, self.okdp)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering	= ('id',)
		verbose_name = u'Работа'
		verbose_name_plural = u'Работы'
	def	exml(self):
		return u'\t<%s id="%d" stage="%d" okdp="%d" name="%s"/>\n' % (self._xmlname, self.id, self.stage.id, self.okdp, self.name)

class	Speciality(models.Model):
	name		= models.CharField(max_length=255, blank=False, unique=True, verbose_name=u'Наименование')
	stages		= models.ManyToManyField(Stage, through='SpecialityStage', verbose_name=u'Виды работ')
	_xmlname	= u'speciality'

	def	asstr(self):
		return u'%s' % (self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering	= ('name',)
		verbose_name	= u'Специальность'
		verbose_name_plural = u'Специальности'

	def	exml(self):
		return u'\t<%s name=\"%s\"/>\n' % (self._xmlname, self.name)

class	SpecialityStage(models.Model):
	speciality	= models.ForeignKey(Speciality, verbose_name=u'Специальность')
	stage		= models.ForeignKey(Stage, verbose_name=u'Вид работ')
	_xmlname	= u'specialitysrage'

	def	asstr(self):
		return u'%s:%s' % (self.speciality, self.stage)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Специальность.ВидРабот'
		verbose_name_plural	= u'Специальности.ВидыРабот'
		unique_together		= (('speciality', 'stage',),)

	def	exml(self):
		return u'\t<%s name=\"%s\"/>\n' % (self._xmlname, self.name)

class	Skill(models.Model):
	'''
	id - by OKSO+qualificationid
	'''
	name		= models.CharField(max_length=50, blank=False, unique=True, verbose_name=u'Наименование')
	high		= models.BooleanField(blank=False, null=False, default=False, verbose_name=u'Высшее')
	_xmlname	= u'skill'
	def	asstr(self):
		return self.name
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('name',)
		verbose_name = u'Квалификация'
		verbose_name_plural = u'Квалификации'
	def	exml(self):
		return u'\t<%s name="%s"/>\n' % (self._xmlname, self.name)

class	File(RenameFilesModel):
	name		= models.CharField	(null=False, blank=False, max_length=255, verbose_name=u'Имя файла')
	mime		= models.CharField	(null=False, blank=False, max_length=255, verbose_name=u'Тип Mime')
	saved		= models.DateTimeField	(null=False, blank=False, auto_now_add=True, verbose_name=u'Записано')
	comments	= models.CharField	(null=False, blank=True, max_length=255, verbose_name=u'Коментарии')
	file		= models.FileField	(null=False, upload_to=my_upload_to, verbose_name=u'Файл')	# attrs: name, path, url, size
	_xmlname	= u'file'
	RENAME_FILES	= {'file': {'dest': '', 'keep_ext': False}}
	def	asstr(self):
		return u'%s : %s' % (self.name, self.comments)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name = u'Файл'
		verbose_name_plural = u'Файлы'
	def	exml(self):
		retvalue = u'\t<%s id="%d" name="%s" mime="%s" saved="%s"' % (self._xmlname, self.id, self.name, self.mime, self.saved)
		if (self.comments):
			retvalue += u' comments="%s"' % self.comments
		return retvalue + '/>\n'
	def	save(self):
		#print "Before save"
		#print self.file.name, self.file.path, self.id, os.path.exists(self.file.path), Mime.get_type(self.file.path)
		self.mime = str(Mime.get_type(self.file.path))
		super(File, self).save()
		#print "After save"
		#print self.file.name, self.file.path

class	EventType(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')
	_xmlname	= u'eventtype'
	def	asstr(self):
		return self.name
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name = u'Тип события'
		verbose_name_plural = u'Типы событий'
	def	exml(self):
		retvalue = u'\t<%s id="%d" name="%s"' % (self._xmlname, self.id, self.name)
		if (self.comments):
			retvalue += u' comments="%s"' % self.comments
		return retvalue + '/>\n'

class	Role(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')
	_xmlname	= u'role'
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
	def	exml(self):
		retvalue = u'\t<%s id="%d" name="%s"' % (self._xmlname, self.id, self.name)
		if (self.comments):
			retvalue += u' comments="%s"' % self.comments
		return retvalue + '/>\n'

class	Person(models.Model):
	firstname	= models.CharField(max_length=16, blank=False, verbose_name=u'Имя')
	midname		= models.CharField(max_length=24, blank=True, verbose_name=u'Отчество')
	lastname	= models.CharField(max_length=24, blank=False, verbose_name=u'Фамилия')
	skills		= models.ManyToManyField(Skill, through='PersonSkill', verbose_name=u'Квалификации')
	files		= models.ManyToManyField(File, through='PersonFile', verbose_name=u'Файлы')
	phone		= models.CharField(null=True, blank=True, max_length=25, verbose_name=u'Телефон')
	_xmlname	= u'person'
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
	def	exml(self):
		retvalue = u'\t<%s id="%d" firstname="%s" lastname="%s"' % (self._xmlname, self.id, self.firstname, self.lastname)
		if (self.midname):
			retvalue += u' midname="%s"' % self.midname
		return retvalue + '/>\n'

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
	_xmlname	= u'personskill'
	def	asstr(self):
		return u'%s: %s, %s' % (self.person.asstr(), self.speciality.asstr(), self.skill.asstr())
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name = u'Человек.Квалификация'
		verbose_name_plural = u'Человек.Квалификации'
	def	exml(self):
		return u'\t<%s id="%d" person="%d" speciality=\"%d\" skill="%d"/>\n' % (self._xmlname, self.id, self.person.id, self.speciality.id, self.skill.id)

class	PersonFile(models.Model):
	person		= models.ForeignKey(Person, verbose_name=u'Человек')
	file		= models.ForeignKey(File, verbose_name=u'Файл')
	_xmlname	= u'personfile'
	def	asstr(self):
		return self.file.asstr()
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'Человек.Файл'
		verbose_name_plural	= u'Человек.Файлы'
		unique_together		= [('person', 'file',)]
	def	exml(self):
		return u'\t<%s id="%d" person="%d" file="%d"/>\n' % (self._xmlname, self.id, self.person.id, self.file.id)

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
	sroregno	= models.PositiveIntegerField(null=True, blank=True, unique=True, verbose_name=u'Реестровый №')
	sroregdate	= models.DateField(null=True, blank=True, verbose_name=u'Дата членства в НП')
	paydate		= models.DateField(null=True, blank=True, verbose_name=u'Дата оплаты взноса в КФ')
	paysum		= models.PositiveIntegerField(null=False, blank=False, verbose_name=u'Сумма взноса в КФ')
	paydatevv	= models.DateField(null=True, blank=True, verbose_name=u'Дата оплаты вступительного взноса')
	comments	= models.TextField(null=True, blank=True, verbose_name=u'Коментарии')
	public		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Публиковать')
	okveds		= models.ManyToManyField(Okved, through='OrgOkved', verbose_name=u'Коды ОКВЭД')
	stuffs		= models.ManyToManyField(Person, through='OrgStuff', verbose_name=u'Штат')
	events		= models.ManyToManyField(EventType, through='OrgEvent', verbose_name=u'События')
	files		= models.ManyToManyField(File, through='OrgFile', verbose_name=u'Файлы')
	_xmlname	= u'org'
	def	asstr(self):
		return self.name
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('name',)
		verbose_name		= u'Организация'
		verbose_name_plural	= u'Организации'
	def	exml(self):
		retvalue = u'\t<%s id="%d" name="%s" fullname="%s" regdate="%s" inn="%d" kpp="%d" ogrn="%d" laddress="%s" okopf="%d"' % (
			self._xmlname,
			self.id,
			self.name,
			self.fullname,
			self.regdate,
			self.inn,
			self.kpp,
			self.ogrn,
			self.laddress,
			self.okopf.id,
		)
		if (self.raddress):
			retvalue += u' raddress="%s"' % self.raddress
		return retvalue + '/>\n'

class	OrgOkved(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	okved		= models.ForeignKey(Okved, verbose_name=u'ОКВЭД')
	_xmlname	= u'orgokved'
	def	asstr(self):
		return self.okved.asstr()
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'Организация.ОКВЭД'
		verbose_name_plural	= u'Организация.Коды ОКВЭД'
		unique_together		= [('org', 'okved')]
	def	exml(self):
		return ''

class	OrgPhone(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	phone		= models.CharField(null=False, blank=False, max_length=25, verbose_name=u'Номер')
	_xmlname	= u'orgphone'
	def	asstr(self):
		return self.phone
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering		= ('id',)
		verbose_name		= u'Телефон'
		verbose_name_plural	= u'Телефоны'
	def	exml(self):
		return u'\t<%s id="%d" phone="%d"/>' % (self._xmlname, self.id, self.phone)

class	OrgEmail(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	URL		= models.EmailField(null=False, blank=False, unique=False, verbose_name=u'Ссылка')
	_xmlname	= u'orgemail'
	def	asstr(self):
		return self.URL
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('URL',)
		verbose_name = u'Электропочта'
		verbose_name_plural = u'Адреса электропочты'
		unique_together		= [('org', 'URL')]
	def	exml(self):
		return u'\t<%s id="%d" URL="%s"/>\n' % (self._xmlname, self.id, self.URL)

class	OrgWWW(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	URL		= models.URLField(blank=False, unique=True, verbose_name=u'Ссылка')
	_xmlname	= u'orgwww'
	def	asstr(self):
		return self.URL
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('URL',)
		verbose_name = u'WWW'
		verbose_name_plural = u'WWW'
		unique_together		= [('org', 'URL')]
	def	exml(self):
		return u'\t<%s id="%d" URL="%s"/>\n' % (self._xmlname, self.id, self.URL)

class	OrgStuff(models.Model):
	'''
	FIXME: permanent => Fulltime job
	'''
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	role		= models.ForeignKey(Role, verbose_name=u'Должность')
	person		= models.ForeignKey(Person, verbose_name=u'Человек')
	leader		= models.BooleanField(verbose_name=u'Руководитель')
	permanent	= models.BooleanField(verbose_name=u'Постоянное место работы')
	_xmlname	= u'orgstuff'
	def	asstr(self):
		return u'%s: %s' % (self.role.asstr(), self.person.asstr())
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'Организация.Должностное лицо'
		verbose_name_plural	= u'Организация.Должностные лица'
		unique_together		= [('org', 'role', 'person')]
	def	exml(self):
		return ''

class	OrgEvent(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	type		= models.ForeignKey(EventType, verbose_name=u'Типа события')
	date		= models.DateField(blank=False, verbose_name=u'Дата')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарий')
	_xmlname	= u'orgevent'
	def	asstr(self):
		return self.type.asstr()
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'Организация.Событие'
		verbose_name_plural	= u'Организация.События'
	def	exml(self):
		return ''

class	OrgFile(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	file		= models.ForeignKey(File, verbose_name=u'Файл')
	_xmlname	= u'orgfile'
	def	asstr(self):
		return self.file.asstr()
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'Организация.Файл'
		verbose_name_plural	= u'Организация.Файлы'
		unique_together		= [('org', 'file')]
	def	exml(self):
		return ''

class	OrgLicense(models.Model):
	org		= models.OneToOneField(Org, verbose_name=u'Организация')
	no		= models.CharField(null=False, blank=False, max_length=100, unique=True, verbose_name=u'Номер лицензии')
	datefrom	= models.DateField(null=False, blank=False, verbose_name=u'Выдана')
	datedue		= models.DateField(null=False, blank=False, verbose_name=u'Действительна до')
	_xmlname	= u'orglicense'
	def	asstr(self):
		return u'%s, до %s' % (self.no, self.datedue)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('org',)
		verbose_name = u'Организация.Лицензия'
		verbose_name_plural = u'Организация.Лицензии'
	def	exml(self):
		return u'\t<%s id="%d" URL="%s"/>\n' % (self._xmlname, self.id, self.insurer)

class	OrgInsurance(models.Model):
	org		= models.OneToOneField(Org, verbose_name=u'Организация')
	insurer		= models.ForeignKey(Insurer, null=True, blank=True, verbose_name=u'Страховщик')
	insno		= models.CharField(null=False, blank=False, unique=True, max_length=50, verbose_name=u'Номер договора')
	insdate		= models.DateField(null=False, blank=False, verbose_name=u'Дата договора')
	insum		= models.PositiveIntegerField(null=False, blank=False, verbose_name=u'Страховая сумма')
	datefrom	= models.DateField(null=True, blank=True, verbose_name=u'Страховка с')
	datetill	= models.DateField(null=True, blank=True, verbose_name=u'Страховка до')
	_xmlname	= u'orginsurance'
	def	asstr(self):
		return u'%s от %s, %d руб, с %s по %s' % (self.insno, self.insdate, self.insum, self.datefrom, self.datetill)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('org',)
		verbose_name = u'Организация.Страховка'
		verbose_name_plural = u'Организация.Страховки'
	def	exml(self):
		return u'\t<%s id="%d" URL="%s"/>\n' % (self._xmlname, self.id, self.insurer)

class	Meeting(models.Model):
	regno		= models.PositiveIntegerField(null=False, blank=False, unique=False, verbose_name=u'№')
	date		= models.DateField(null=False, blank=False, verbose_name=u'Дата')
	common		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Общее')
	agenda		= models.CharField(max_length=100, null=False, blank=False, verbose_name=u'Повестка')
	log		= models.TextField(null=True, blank=True, verbose_name=u'Протокол')
	orgs		= models.ManyToManyField(Org, through='MeetingOrg', verbose_name=u'Организации')
	_xmlname	= u'meeting'
	def	asstr(self):
		return u'№ %d от %s' % (self.regno, self.date)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('date',)
		verbose_name		= u'Заседание'
		verbose_name_plural	= u'Заседания'
	def	exml(self):
		return u'\t<%s id="%d" date="%s" agenda="%s" log="%s"/>\n' % (self._xmlname, self.id, self.date, self.agenda, self.log)

class	MeetingOrg(models.Model):
	meeting		= models.ForeignKey(Meeting, verbose_name=u'Заседание')
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	_xmlname	= u'meetingorg'
	def	asstr(self):
		return self.org.asstr()
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('meeting',)
		verbose_name		= u'Заседание.Организация'
		verbose_name_plural	= u'Заседание.Организации'
		unique_together		= [('meeting', 'org')]
	def	exml(self):
		return ''

class	PermitType(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=30, blank=False, unique=True, verbose_name=u'Наименование')
	_xmlname	= u'permit'
	def	asstr(self):
		return u'%d: %s' % (self.id, self.name)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'СписокВидовРаботТип'
		verbose_name_plural	= u'СписокВидовРаботТипы'
	def	exml(self):
		return ''

class	Permit(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	permittype	= models.ForeignKey(PermitType, verbose_name=u'Тип')
	stages		= models.ManyToManyField(Stage, through='PermitStage', verbose_name=u'Виды работ')
	#stages		= CheckBoxManyToMany(Stage, through='PermitStage', verbose_name=u'Виды работ')
	_xmlname	= u'permit'
	def	asstr(self):
		return u'%s: %s' % (self.org.asstr(), self.permittype.name)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'СписокВидовРабот'
		verbose_name_plural	= u'СпискиВидовРабот'
	def	exml(self):
		return ''

class	PermitStage(models.Model):
	permit		= models.ForeignKey(Permit, verbose_name=u'Разрешение')
	stage		= models.ForeignKey(Stage, verbose_name=u'Вид работ')
	jobs		= models.ManyToManyField(Job, through='PermitStageJob', verbose_name=u'Работы')
	_xmlname	= u'permitstage'
	def	asstr(self):
		return u'%s: %s' % (self.permit.asstr(), self.stage.asstr())
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'СписокВидовРабот.ВидРабот'
		verbose_name_plural	= u'СписокВидовРабот.ВидыРабот'
		unique_together		= [('permit', 'stage')]
	def	exml(self):
		return ''

class	PermitStageJob(models.Model):
	permitstage	= models.ForeignKey(PermitStage, verbose_name=u'Разрешение.Вид работ')
	job		= models.ForeignKey(Job, verbose_name=u'Работа')	#, limit_choices_to = { 'permit_stage__eq': self.permitstage.stage })
	_xmlname	= u'permitstagejob'
	def	asstr(self):
		return u'%s: %s' % (self.permitstage.asstr(), self.job.asstr())
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'СписокВидовРабот.ВидРабот.Работа'
		verbose_name_plural	= u'СписокВидовРабот.ВидРабот.Работы'
		unique_together		= [('permitstage', 'job')]
	def	exml(self):
		return ''

class	PermitOwn(models.Model):
	permit		= models.OneToOneField(Permit, verbose_name=u'СписокВидовРабот')
	regno		= models.PositiveIntegerField(null=False, blank=False, unique=False, verbose_name=u'№')
	date		= models.DateField(null=True, blank=True, verbose_name=u'Дата')
	datedue		= models.DateField(null=True, blank=True, verbose_name=u'Дата аннулирования')
	meeting		= models.ForeignKey(Meeting, null=True, blank=True, verbose_name=u'Заседание')
	_xmlname	= u'permitown'
	def	asstr(self):
		return u'%s: %s № %d от %s' % (self.permit.org.name, self.permit.permittype.name, self.regno, self.permit.date)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'СвидетельствоСобственное'
		verbose_name_plural	= u'СвидетельстваСобственные'
	def	exml(self):
		return ''

class	PermitStatement(models.Model):
	permit		= models.OneToOneField(Permit, verbose_name=u'СписокВидовРабот')
	date		= models.DateField(null=True, blank=True, verbose_name=u'Дата')
	_xmlname	= u'permitstatement'
	def	asstr(self):
		return u'%s: %s № %d от %s' % (self.permit.org.name, self.permit.permittype.name, self.regno, self.permit.date)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'Заявление'
		verbose_name_plural	= u'Заявления'
	def	exml(self):
		return ''

class	SRO(models.Model):
	name		= models.CharField(max_length=30,  blank=False, unique=True, verbose_name=u'Наименование')
	fullname	= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Полное наименование')
	regno		= models.CharField(max_length=30,  blank=False, unique=True, verbose_name=u'Рег. №')
	_xmlname	= u'sro'
	def	asstr(self):
		return self.name
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering		= ('name',)
		verbose_name		= u'СРО'
		verbose_name_plural	= u'СРО'
	def	exml(self):
		return ''

class	PermitAlien(models.Model):
	permit		= models.OneToOneField(Permit, verbose_name=u'СписокВидовРабот')
	sro		= models.ForeignKey(SRO, null=False, blank=False, verbose_name=u'СРО')
	regno		= models.CharField(max_length=50, null=False, blank=False, unique=False, verbose_name=u'Рег. №')
	date		= models.DateField(null=False, blank=False, verbose_name=u'Дата')
	protono		= models.CharField(max_length=16, null=False, blank=False, unique=False, verbose_name=u'Протокол №')
	protodate	= models.DateField(null=False, blank=False, verbose_name=u'Дата протокола')
	_xmlname	= u'permitalien'
	def	asstr(self):
		return u'%s: %s № %d от %s' % (self.permit.org.name, self.permit.permittype.name, self.regno, self.permit.date)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		verbose_name		= u'СвидетельствоЧужое'
		verbose_name_plural	= u'СвидетельстваЧужие'
	def	exml(self):
		return ''

# Projecting addon
class	PrjStage(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=255, blank=False, unique=True, verbose_name=u'Наименование')
	hq		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Кол-во ВО', help_text=u'Количество специалистов с высшим образованием')
	hs		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Стаж ВО', help_text=u'Минимальный стаж специалистов с высшим образованием')
	mq		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Кол-во СО', help_text=u'Количество специалистов со средним образованием')
	ms		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Стаж СО', help_text=u'Минимальный стаж специалистов со средним образованием')
	def	asstr(self):
		return u'%02d. %s' % (self.id, self.name)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('id',)
		verbose_name = u'Prj: Вид работ'
		verbose_name_plural = u'Prj: Виды работ'

class	PrjProto(models.Model):
	no		= models.PositiveSmallIntegerField(null=False, blank=False, verbose_name=u'№ протокола')
	date		= models.DateField(null=False, blank=False, verbose_name=u'Дата протокола')
	def	asstr(self):
		return u'%d от %s' % (self.no, self.date)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('no',)
		verbose_name = u'Prj: Протокол'
		verbose_name_plural = u'Prj: Протоколы'

class	PrjOrg(models.Model):
	org		= models.OneToOneField(Org, verbose_name=u'Организация')
	# 1. SRO
	regno		= models.CharField(max_length=50, null=True, blank=True, unique=False, verbose_name=u'Рег. №')
	regdate		= models.DateField(null=True, blank=True, verbose_name=u'Дата членства')
	paydate		= models.DateField(null=True, blank=True, verbose_name=u'Дата оплаты взноса в КФ')
	paysum		= models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Сумма взноса в КФ')
	paydatevv	= models.DateField(null=True, blank=True, verbose_name=u'Дата оплаты вступительного взноса')
	# 2. license
	licno		= models.CharField(null=True, blank=True, max_length=100, unique=True, verbose_name=u'Лиц №')
	licfrom		= models.DateField(null=True, blank=True, verbose_name=u'Лиц. выдана')
	licdue		= models.DateField(null=True, blank=True, verbose_name=u'Лиц. до')
	# 3. insurance
	insurer		= models.ForeignKey(Insurer, null=True, blank=True, verbose_name=u'Страховщик')
	insno		= models.CharField(null=True, blank=True, unique=True, max_length=50, verbose_name=u'Номер договора')
	insdate		= models.DateField(null=True, blank=True, verbose_name=u'Дата договора')
	inssum		= models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Страховая сумма')
	insfrom		= models.DateField(null=True, blank=True, verbose_name=u'Страховка с')
	insdue		= models.DateField(null=True, blank=True, verbose_name=u'Страховка до')
	# 4. misc
	publish		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Публиковать')
	projonly	= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Только проектирование')
	comments	= models.TextField(null=True, blank=True, verbose_name=u'Коментарии')
	# 5. permision
	permno		= models.CharField(max_length=16, null=True, blank=True, unique=False, verbose_name=u'Свид. №')
	permdate	= models.DateField(null=True, blank=True, verbose_name=u'Свид. дата')
	protocol	= models.ForeignKey(PrjProto, null=True, blank=True, verbose_name=u'Протокол')
	stages		= models.ManyToManyField(PrjStage, through='PrjOrgStage', verbose_name=u'Виды работ')
	def	asstr(self):
		return u'%s' % self.org
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('org',)
		verbose_name		= u'Prj: Организация'
		verbose_name_plural	= u'Prj: Организации'

class	PrjOrgStage(models.Model):
	org		= models.ForeignKey(PrjOrg, null=False, blank=False, verbose_name=u'Организация')
	stage		= models.ForeignKey(PrjStage, null=False, blank=False, verbose_name=u'Вид работ')
	def	asstr(self):
		return u'%s: %s' % (self.org, self.stage)
	def	__unicode__(self):
		return self.asstr()
	class	Meta:
		ordering = ('org', 'stage')
		verbose_name		= u'Prj: Организация.ВидРабот'
		verbose_name_plural	= u'Prj: Организации.ВидыРабот'

modellist = (
	Insurer, Okato, Okopf, Okved, Speciality, SpecialityStage, Skill, Stage, Job, File,
	EventType, Role, Person, PersonSkill, PersonFile, Org, OrgOkved, OrgPhone, OrgEmail, OrgWWW,
	OrgStuff, OrgEvent, OrgFile, OrgLicense, OrgInsurance, Meeting, MeetingOrg, PermitType, Permit, PermitStage,
	PermitStageJob, PermitOwn, PermitStatement, SRO, PermitAlien, PrjStage, PrjProto, PrjOrg, PrjOrgStage
)
