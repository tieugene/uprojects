# -*- coding: utf-8 -*-
'''
models: 30 (w/o country & trunk)
'''

from django.db import models
from rfm import RenameFilesModel
from xdg import Mime
import os

class	Okopf(models.Model):
	'''
	id - by OKOPF, short int
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
	shortname	= models.CharField(max_length=10, null=True, blank=True, verbose_name=u'Краткое наименование')
	disabled	= models.BooleanField(blank=False, verbose_name=u'Не выбирать')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')
	_xmlname		= u'okopf'

	def	asstr(self):
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
	disabled	= models.BooleanField(blank=False, verbose_name=u'Не выбирать')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')
	_xmlname		= u'okved'

	def	fmtid(self):
		l = len(self.id)
		if (l < 3):
			return id
		elif (l > 4):
			return u'%s.%s.%s' % (self.id[:2], self.id[2:4], self.id[4:])
		else:
			return u'%s.%s' % (self.id[:2], self.id[2:])

	def	asstr(self):
		return u'%s %s' % (self.fmtid(), self.name)

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

class	Okso(models.Model):
	'''
	id - by OKSO, int
	'''
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=255, blank=False, unique=False, verbose_name=u'Наименование')
	disabled	= models.BooleanField(blank=False, verbose_name=u'Не выбирать')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')
	_xmlname		= u'okso'

	def	asstr(self):
		return u'%06d %s' % (self.id, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКСО'
		verbose_name_plural = u'Коды ОКСО'

	def	exml(self):
		retvalue = u'\t<%s id="%06d" name="%s"' % (self._xmlname, self.id, self.name)
		if (self.disabled):
			retvalue += u' disabled="1"'
		if (self.parent):
			retvalue += u' parent="%d"' % self.parent
		return retvalue + u'/>\n'

class	Skill(models.Model):
	'''
	id - by OKSO+qualificationid
	'''
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Код')
	okso		= models.ForeignKey(Okso, verbose_name=u'Код ОКСО')
	skill		= models.PositiveSmallIntegerField(blank=False, verbose_name=u'Код квалилфикации')
	name		= models.CharField(max_length=50, blank=False, verbose_name=u'Наименование')
	_xmlname	= u'skill'

	def	asstr(self):
		return u'%06d%d %s' % (self.okso.id, self.skill, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'Квалификация'
		verbose_name_plural = u'Квалификации'

	def	exml(self):
		return u'\t<%s id="%09d" okso="%06d" skill="%d" name="%s"/>\n' % (self._xmlname, self.id, self.okso.id, self.skill, self.name)

class	Okdp(models.Model):
	'''
	id - by OKDP, int
	'''
	id		= models.CharField(max_length=7, primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=255, blank=False, unique=False, verbose_name=u'Наименование')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')
	_xmlname	= u'okdp'

	def	asstr(self):
		return u'%7s %s' % (self.id, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'ОКДП'
		verbose_name_plural = u'Коды ОКДП'

	def	exml(self):
		retvalue = u'\t<%s id="%s" name="%s"' % (self._xmlname, self.id, self.name)
		if (self.parent):
			retvalue += u' parent="%s"' % self.parent
		return retvalue + u'/>\n'

class	Stage(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=255, blank=False, unique=True, verbose_name=u'Наименование')
	hq		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Кол-во ВО', help_text=u'Количество специалистов с высшим образованием')
	hs		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Стаж ВО', help_text=u'Минимальный стаж специалистов с высшим образованием')
	mq		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Кол-во СО', help_text=u'Количество специалистов со средним образованием')
	ms		= models.PositiveSmallIntegerField(null=True, verbose_name=u'Стаж СО', help_text=u'Минимальный стаж специалистов со средним образованием')
	oksos		= models.ManyToManyField(Okso, through='StageOkso', verbose_name=u'Коды ОКСО')
	jobs		= models.ManyToManyField(Okdp, through='Job', verbose_name=u'Виды работ')
	_xmlname	= u'stage'

	def	asstr(self):
		return u'%02d %s' % (self.id, self.name)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'Группа работ'
		verbose_name_plural = u'Группы работ'

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

class	StageOkso(models.Model):
	stage		= models.ForeignKey(Stage, verbose_name=u'Группа работ')
	okso		= models.ForeignKey(Okso, verbose_name=u'ОКСО')
	_xmlname	= u'stageokso'

	def	asstr(self):
		return self.okso.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name = u'Группа работ.ОКСО'
		verbose_name_plural = u'Группы работ.ОКСО'

	def	exml(self):
		return u'\t<%s id="%d" stage="%d" okso="%d"/>\n' % (self._xmlname, self.id, self.stage.id, self.okso.id)

class	Job(models.Model):
	stage		= models.ForeignKey(Stage, verbose_name=u'Группа работ')
	okdp		= models.ForeignKey(Okdp, verbose_name=u'ОКДП')
	_xmlname	= u'job'

	def	asstr(self):
		return u'%02d: %s' % (self.stage.id, self.okdp.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name = u'Вид работ'
		verbose_name_plural = u'Виды работ'

	def	exml(self):
		return u'\t<%s id="%d" stage="%d" okdp="%s"/>\n' % (self._xmlname, self.id, self.stage.id, self.okdp.id)

class	Phone(models.Model):
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Номер')
	country		= models.PositiveIntegerField(blank=False, verbose_name=u'Код страны')
	trunk		= models.PositiveIntegerField(blank=False, verbose_name=u'Код магистрали')
	phone		= models.DecimalField(max_digits=7, decimal_places=0, blank=False, verbose_name=u'Номер')
	ext		= models.DecimalField(max_digits=4, decimal_places=0, blank=True, verbose_name=u'Доб.')
	_xmlname	= u'phone'

	def	asstr(self):
		if (self.ext):
			e = u' #%d' % self.ext
		else:
			e = ''
		return u'+%d %d %s%s' % (self.country, self.trunk, self.phone, e)

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('id',)
		verbose_name = u'Номер телефона'
		verbose_name_plural = u'Номера телефонов'

	def	exml(self):
		retvalue = u'\t<%s id="%d" country="%d" trunk="%d" phone="%d"' % (self._xmlname, self.id, self.country, self.trunk, self.phone)
		if (self.ext):
			retvalue += u' ext="%d"' % self.ext
		return retvalue + '/>\n'

class	Email(models.Model):
	URL		= models.EmailField(blank=False, unique=True, verbose_name=u'Ссылка')
	_xmlname	= u'email'

	def	asstr(self):
		return self.URL

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('URL',)
		verbose_name = u'Электропочта'
		verbose_name_plural = u'Адреса электропочты'

	def	exml(self):
		return u'\t<%s id="%d" URL="%s"/>\n' % (self._xmlname, self.id, self.URL)

def	my_upload_to(instance, filename):
	"""Generates upload path for FileField"""
	instance.name = filename
	return u'temp/%s' % filename

class	File(RenameFilesModel):
	name		= models.CharField	(null=False, blank=False, max_length=255, verbose_name=u'Имя файла')
	mime		= models.CharField	(null=False, blank=False, max_length=255, verbose_name=u'Тип Mime')
	saved		= models.DateTimeField	(null=False, blank=False, auto_now_add=True, verbose_name=u'Записано')
	comments	= models.CharField	(null=False, blank=True, max_length=255, verbose_name=u'Коментарии')
	file		= models.FileField	(null=False, upload_to=my_upload_to, verbose_name=u'Файл')
	''' attrs: name, path, url, size '''
	_xmlname		= u'file'
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
	_xmlname		= u'role'

	def	asstr(self):
		return self.name

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
	_xmlname		= u'person'

	def	asstr(self):
		return u'%s %s %s' % (self.lastname, self.firstname, self.midname)

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
	skill		= models.ForeignKey(Skill, verbose_name=u'Квалификация')
	_xmlname		= u'personskill'

	def	asstr(self):
		return u'%s: %s' % (self.person.asstr(), self.skill.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name = u'Человек.Квалификация'
		verbose_name_plural = u'Человек.Квалификации'

	def	exml(self):
		return u'\t<%s id="%d" person="%d" skill="%d"/>\n' % (self._xmlname, self.id, self.person.id, self.skill.id)

class	PersonFile(models.Model):
	person		= models.ForeignKey(Person, verbose_name=u'Человек')
	file		= models.ForeignKey(File, verbose_name=u'Файл')
	_xmlname		= u'personfile'

	def	asstr(self):
		return self.file.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name = u'Человек.Файл'
		verbose_name_plural = u'Человек.Файлы'

	def	exml(self):
		return u'\t<%s id="%d" person="%d" file="%d"/>\n' % (self._xmlname, self.id, self.person.id, self.file.id)

class	Org(models.Model):
	name		= models.CharField(null=False, blank=False, max_length=40, unique=True, verbose_name=u'Наименование')
	fullname	= models.CharField(null=False, blank=False, max_length=100, unique=False, verbose_name=u'Полное наименование')
	regdate		= models.DateField(null=False, verbose_name=u'Дата регистрации')
	inn		= models.PositiveIntegerField(null=False, verbose_name=u'ИНН')
	kpp		= models.PositiveIntegerField(null=False, verbose_name=u'КПП')
	ogrn		= models.PositiveIntegerField(null=False, verbose_name=u'ОГРН')
	laddress	= models.CharField(null=False, blank=False, max_length=100, verbose_name=u'Адрес юридический')
	raddress	= models.CharField(null=True, blank=True, max_length=100, verbose_name=u'Адрес почтовый')
	sroregdate	= models.DateField(null=True, verbose_name=u'Дата регистрации в СРО')
	licno		= models.CharField(null=True, blank=True, max_length=30, verbose_name=u'Номер лицензии')
	licdue		= models.DateField(null=True, verbose_name=u'Лицензия действительна до')
	okopf		= models.ForeignKey(Okopf, null=False, verbose_name=u'ОКОПФ')
	okveds		= models.ManyToManyField(Okved, through='OrgOkved', verbose_name=u'Коды ОКВЭД')
	lokdps		= models.ManyToManyField(Okdp, through='OrgLOkdp', verbose_name=u'Коды ОКДП по лицензии')
	stages		= models.ManyToManyField(Stage, through='OrgStage', verbose_name=u'Группы видов работ')
	phones		= models.ManyToManyField(Phone, through='OrgPhone', verbose_name=u'Телефоны')
	emails		= models.ManyToManyField(Email, through='OrgEmail', verbose_name=u'Адреса электропочты')
	events		= models.ManyToManyField(EventType, through='OrgEvent', verbose_name=u'События')	# ? + OKDP? - but OKDP can B blank
	stuffs		= models.ManyToManyField(Person, through='OrgStuff', verbose_name=u'Штат')	# ? + Person
	files		= models.ManyToManyField(File, through='OrgFile', verbose_name=u'Файлы')
	_xmlname		= u'org'

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

	def	exml(self):
		return ''

class	OrgLOkdp(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	okdp		= models.ForeignKey(Okdp, verbose_name=u'ОКДП по лицензии')
	_xmlname		= u'orglokdp'

	def	asstr(self):
		return self.okdp.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.ОКДП по лицензии'
		verbose_name_plural	= u'Организация.Коды ОКДП по лицензии'

	def	exml(self):
		return ''

class	OrgStage(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	stage		= models.ForeignKey(Stage, verbose_name=u'Группа работ')
	jobs		= models.ManyToManyField(Job, through='OrgJob', verbose_name=u'Виды работ')
	_xmlname		= u'orgstage'

	def	asstr(self):
		return u'%s: %s' % (self.org.asstr(), self.stage.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Группа работ'
		verbose_name_plural	= u'Организация.Группы работ'

	def	exml(self):
		return ''

class	OrgJob(models.Model):
	orgstage	= models.ForeignKey(OrgStage, verbose_name=u'Организация.Группа работ')
	job		= models.ForeignKey(Job, verbose_name=u'Вид работ')
	_xmlname		= u'orgjob'

	def	asstr(self):
		return u'%s: %s' % (self.orgstage.asstr(), self.job.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Вид работ'
		verbose_name_plural	= u'Организация.Виды работ'

	def	exml(self):
		return ''

class	OrgPhone(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	phone		= models.ForeignKey(Phone, verbose_name=u'Телефон')
	_xmlname		= u'orgphone'

	def	asstr(self):
		return self.phone.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Телефон'
		verbose_name_plural	= u'Организация.Телефоны'

	def	exml(self):
		return ''

class	OrgEmail(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	email		= models.ForeignKey(Email, verbose_name=u'Электропочта')
	_xmlname		= u'orgemail'

	def	asstr(self):
		return self.email.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Электропочта'
		verbose_name_plural	= u'Организация.Адреса электропочты'

	def	exml(self):
		return ''

class	OrgEvent(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	type		= models.ForeignKey(EventType, verbose_name=u'Типа события')
	date		= models.DateField(blank=False, verbose_name=u'Дата')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарий')
	stages		= models.ManyToManyField(Stage, through='OrgEventStage', verbose_name=u'Группы видов работ')
	_xmlname		= u'orgevent'

	def	asstr(self):
		return self.type.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Событие'
		verbose_name_plural	= u'Организация.События'

	def	exml(self):
		return ''

class	OrgEventStage(models.Model):
	orgevent	= models.ForeignKey(OrgEvent, verbose_name=u'Организация.Событие')
	stage		= models.ForeignKey(Stage, verbose_name=u'Группа работ')
	jobs		= models.ManyToManyField(Job, through='OrgEventJob', verbose_name=u'Виды работ')
	_xmlname		= u'orgeventstage'

	def	asstr(self):
		return self.stage.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Событие.Группа работ'
		verbose_name_plural	= u'Организация.Событие.Группы работ'

	def	exml(self):
		return ''

class	OrgEventJob(models.Model):
	orgeventstage	= models.ForeignKey(OrgEventStage, verbose_name=u'Организация.Событие.Группа работ')
	job		= models.ForeignKey(Job, verbose_name=u'Вид работ')
	_xmlname		= u'orgeventjob'

	def	asstr(self):
		return self.job.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Событие.Вид работ'
		verbose_name_plural	= u'Организация.Событие.Виды работ'

	def	exml(self):
		return ''

class	OrgStuff(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	role		= models.ForeignKey(Role, verbose_name=u'Должность')
	person		= models.ForeignKey(Person, verbose_name=u'Человек')
	leader		= models.BooleanField(verbose_name=u'Начальство')
	_xmlname		= u'orgstuff'

	def	asstr(self):
		return u'%s: %s' % (self.role.asstr(), self.person.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Должностное лицо'
		verbose_name_plural	= u'Организация.Должностные лица'

	def	exml(self):
		return ''

class	OrgFile(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	file		= models.ForeignKey(File, verbose_name=u'Файл')
	_xmlname		= u'orgfile'

	def	asstr(self):
		return self.file.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Файл'
		verbose_name_plural	= u'Организация.Файлы'

	def	exml(self):
		return ''

class	Meeting(models.Model):
	date		= models.DateField(blank=False, verbose_name=u'Дата')
	agenda		= models.CharField(max_length=100, blank=False, verbose_name=u'Повестка')
	log		= models.TextField(blank=True, verbose_name=u'Протокол')
	orgs		= models.ManyToManyField(Org, through='MeetingOrg', verbose_name=u'Организации')
	_xmlname	= u'meeting'

	def	asstr(self):
		return u'%s %s' % (self.date, self.agenda)

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
	_xmlname		= u'meetingorg'

	def	asstr(self):
		return self.org.asstr()

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('meeting',)
		verbose_name		= u'Заседание.Организация'
		verbose_name_plural	= u'Заседание.Организации'

	def	exml(self):
		return ''

modellist = (Okopf, Okved, Okso, Skill, Okdp, Stage, StageOkso, Job, Phone, Email, File, EventType, Role, Person, PersonSkill, PersonFile, Org, OrgOkved, OrgLOkdp, OrgStage, OrgPhone, OrgEmail, OrgEvent, OrgStuff, OrgFile, Meeting, MeetingOrg)
