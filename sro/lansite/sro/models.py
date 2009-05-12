# -*- coding: utf-8 -*-
from django.db import models

class	Okopf(models.Model):
	'''
	id - by OKOPF, short int
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=100, blank=False, unique=True, verbose_name=u'Наименование')
	shortname	= models.CharField(max_length=10, null=True, blank=True, verbose_name=u'Краткое наименование')
	disabled	= models.BooleanField(blank=False, verbose_name=u'Не выбирать')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')
	xmlname		= u'okopfs'

	def	__unicode__(self):
		return self.name

	class	Meta:
		ordering = ['id']
		verbose_name = u'Код ОКОПФ'
		verbose_name_plural = u'Коды ОКОПФ'

	def	exml(self):
		retvalue = u'\t<okopf id="%d" name="%s"' % (self.id, self.name)
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
	xmlname		= u'okveds'

	def	fmtid(self):
		l = len(self.id)
		if (l < 3):
			return id
		elif (l > 4):
			return u'%s.%s.%s' % (self.id[:2], self.id[2:4], self.id[4:])
		else:
			return u'%s.%s' % (self.id[:2], self.id[2:])

	def	__unicode__(self):
		return u'%s %s' % (self.fmtid(), self.name)

	class Meta:
		ordering = ['id']
		verbose_name = u'Код ОКВЭД'
		verbose_name_plural = u'Коды ОКВЭД'

	def	exml(self):
		retvalue = u'\t<okved id="%s" name="%s"' % (self.id, self.name)
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
	xmlname		= u'oksos'

	def	__unicode__(self):
		return u'%06d %s' % (self.id, self.name)

	class Meta:
		ordering = ['id']
		verbose_name = u'Код ОКСО'
		verbose_name_plural = u'Коды ОКСО'

	def	exml(self):
		retvalue = u'\t<okso id="%06d" name="%s"' % (self.id, self.name)
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
	xmlname		= u'skills'

	def	__unicode__(self):
		return u'%06d%d %s' % (self.okso.id, self.skill, self.name)

	class Meta:
		ordering = ['id']
		verbose_name = u'Квалификация'
		verbose_name_plural = u'Квалификации'

	def	exml(self):
		return u'\t<skill id="%09d" okso="%06d" skill="%d" name="%s"/>\n' % (self.id, self.okso.id, self.skill, self.name)

class	Okdp(models.Model):
	'''
	id - by OKDP, int
	'''
	id		= models.CharField(max_length=7, primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=255, blank=False, unique=False, verbose_name=u'Наименование')
	parent		= models.ForeignKey('self', null=True, verbose_name=u'Группа')
	xmlname		= u'okdps'

	def	__unicode__(self):
		return u'%7s %s' % (self.id, self.name)

	class Meta:
		ordering = ['id']
		verbose_name = u'Код ОКДП'
		verbose_name_plural = u'Коды ОКДП'

	def	exml(self):
		retvalue = u'\t<okdp id="%s" name="%s"' % (self.id, self.name)
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
	oksos		= models.ManyToManyField(Okso, through='StageOkso', verbose_name=u'Код ОКСО')
	okdps		= models.ManyToManyField(Okdp, through='StageOkdp', verbose_name=u'Код ОКДП')
	xmlname		= u'stages'

	def	__unicode__(self):
		return u'%02d %s' % (self.id, self.name)

	class Meta:
		ordering = ['id']
		verbose_name = u'Вид работ'
		verbose_name_plural = u'Виды работ'

	def	exml(self):
		retvalue = u'\t<stage id="%d" name="%s"' % (self.id, self.name)
		if (self.hq):
			retvalue += u' hq="%d"' % self.hq
		if (self.hs):
			retvalue += u' hs="%d"' % self.hs
		if (self.mq):
			retvalue += u' mq="%d"' % self.mq
		if (self.ms):
			retvalue += u' ms="%d"' % self.ms
		return retvalue + u'/>\n'

class	StageOkdp(models.Model):
	stage		= models.ForeignKey(Stage)
	okdp		= models.ForeignKey(Okdp)
	xmlname		= u'stageokdps'

	class Meta:
		verbose_name = u'Код ОКДП вида работ'
		verbose_name_plural = u'Коды ОКДП видов работ'

	def	exml(self):
		return u'\t<stageokdp id="%d" stage="%d" okdp="%s"/>\n' % (self.id, self.stage.id, self.okdp.id)

class	StageOkso(models.Model):
	stage		= models.ForeignKey(Stage)
	okso		= models.ForeignKey(Okso)
	xmlname		= u'stageoksos'

	def	__unicode__(self):
		return self.okso.name

	class Meta:
		verbose_name = u'Код ОКСО вида работ'
		verbose_name_plural = u'Коды ОКСО видов работ'

	def	exml(self):
		return u'\t<stageokso id="%d" stage="%d" okso="%d"/>\n' % (self.id, self.stage.id, self.okso.id)

class	Phone(models.Model):
	id		= models.PositiveIntegerField(primary_key=True, verbose_name=u'Номер')
	country		= models.PositiveIntegerField(blank=False, verbose_name=u'Код страны')
	trunk		= models.PositiveIntegerField(blank=False, verbose_name=u'Код магистрали')
	phone		= models.DecimalField(max_digits=7, decimal_places=0, blank=False, verbose_name=u'Номер')
	ext		= models.DecimalField(max_digits=4, decimal_places=0, null=True, verbose_name=u'Доб.')
	xmlname		= u'phones'

	def	__unicode__(self):
		if (ext):
			e = u' #%d' % self.ext
		else:
			e = ''
		return u'+%d %d %s%s' % (self.country, self.trunk, self.phone, ext)

	class Meta:
		ordering = ['id']
		verbose_name = u'Номер телефона'
		verbose_name_plural = u'Номера телефонов'

	def	exml(self):
		retvalue = u'\t<phone id="%d" country="%d" trunk="%d" phone="%d"' % (self.id, self.country, self.trunk, self.phone)
		if (self.ext):
			retvalue += u' ext="%d"' % self.ext
		return retvalue + '/>\n'

class	Email(models.Model):
	URL		= models.EmailField(blank=False, unique=True, verbose_name=u'Ссылка')
	xmlname		= u'emails'

	def	__unicode__(self):
		return self.URL

	class Meta:
		ordering = ['URL']
		verbose_name = u'Адрес электропочты'
		verbose_name_plural = u'Адреса электропочты'

	def	exml(self):
		return u'\t<email id="%d" URL="%s"/>\n' % (self.id, self.URL)

class	File(models.Model):
	name		= models.CharField(max_length=255, blank=False, verbose_name=u'Имя файла')
	mime		= models.CharField(max_length=255, blank=False, verbose_name=u'Тип Mime')
	saved		= models.DateTimeField(blank=False, verbose_name=u'Записано')
	comments	= models.CharField(max_length=255, blank=True, verbose_name=u'Коментарии')
	xmlname		= u'file'

	def	__unicode__(self):
		return self.comments

	class Meta:
		verbose_name = u'Файл'
		verbose_name_plural = u'Файлы'

	def	exml(self):
		retvalue = u'\t<file id="%d" name="%s" mime="%s" saved="%d"' % (self.id, self.name, self.mime, self.saved)
		if (self.comments):
			retvalue += u' comments="%s"' % self.comments
		return retvalue + '/>\n'

class	EventType(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')
	xmlname		= u'eventtypes'

	def	__unicode__(self):
		return self.name

	class Meta:
		verbose_name = u'Тип события'
		verbose_name_plural = u'Типы событий'

	def	exml(self):
		retvalue = u'\t<eventtype id="%d" name="%s"' % (self.id, self.name)
		if (self.comments):
			retvalue += u' comments="%s"' % self.comments
		return retvalue + '/>\n'

class	Role(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True, verbose_name=u'Наименование')
	comments	= models.CharField(max_length=100, blank=True, verbose_name=u'Коментарии')
	xmlname		= u'roles'

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = u'Должность'
		verbose_name_plural = u'Должности'

	def	exml(self):
		retvalue = u'\t<role id="%d" name="%s"' % (self.id, self.name)
		if (self.comments):
			retvalue += u' comments="%s"' % self.comments
		return retvalue + '/>\n'


class	Person(models.Model):
	firstname	= models.CharField(max_length=16, blank=False, verbose_name=u'Имя')
	midname		= models.CharField(max_length=24, blank=True, verbose_name=u'Отчество')
	lastname	= models.CharField(max_length=24, blank=False, verbose_name=u'Фамилия')
	skills		= models.ManyToManyField(Skill, through='PersonSkill', verbose_name=u'Квалификации')
	files		= models.ManyToManyField(File, through='PersonFile', verbose_name=u'Файлы')
	xmlname		= u'persons'

	def	__unicode__(self):
		return u'%s %s %s' % (self.lastname, self.firstname, self.midname)

	class Meta:
		ordering = ['lastname', 'firstname', 'midname']
		verbose_name = u'Человек'
		verbose_name_plural = u'Люди'

	def	exml(self):
		retvalue = u'\t<person id="%d" firstname="%s" lastname="%s"' % (self.id, self.firstname, self.lastname)
		if (self.midname):
			retvalue += u' midname="%s"' % self.midname
		return retvalue + '/>\n'

class	PersonSkill(models.Model):
	person		= models.ForeignKey(Person)
	skill		= models.ForeignKey(Skill)
	xmlname		= u'personskills'

	class Meta:
		verbose_name = u'Квалификация человек'
		verbose_name_plural = u'Квалификации людей'

	def	exml(self):
		return u'\t<personskill id="%d" person="%d" skill="%d"/>\n' % (self.id, self.person.id, self.skill.id)

class	PersonFile(models.Model):
	person		= models.ForeignKey(Person)
	file		= models.ForeignKey(File)
	xmlname		= u'personfiles'

	class Meta:
		verbose_name = u'Файл человека'
		verbose_name_plural = u'Файлы людей'

	def	exml(self):
		return u'\t<personfile id="%d" person="%d" file="%d"/>\n' % (self.id, self.person.id, self.file.id)

class	Org(models.Model):
	name		= models.CharField(blank=False, max_length=40, unique=True, verbose_name=u'Наименование')
	fullname	= models.CharField(blank=False, max_length=100, unique=False, verbose_name=u'Полное наименование')
	regdate		= models.DateField(null=False, verbose_name=u'Дата регистрации')
	inn		= models.PositiveIntegerField(null=False, verbose_name=u'ИНН')
	kpp		= models.PositiveIntegerField(null=False, verbose_name=u'КПП')
	ogrn		= models.PositiveIntegerField(null=False, verbose_name=u'ОГРН')
	laddress	= models.CharField(blank=False, max_length=100, verbose_name=u'Адрес юридический')
	raddress	= models.CharField(null=True, max_length=100, verbose_name=u'Адрес почтовый')
	sroregdate	= models.DateField(null=True, verbose_name=u'Дата регистрации в СРО')
	licno		= models.CharField(null=True, max_length=30, verbose_name=u'Номер лицензии')
	licdue		= models.DateField(null=True, verbose_name=u'Лицензия действительна до')
	okopf		= models.ForeignKey(Okopf, null=False, verbose_name=u'ОКОПФ')
	okveds		= models.ManyToManyField(Okved, through='OrgOkved', verbose_name=u'Коды ОКВЭД')
	lokdps		= models.ManyToManyField(Okdp, through='OrgLOkdp', related_name='lokdp', verbose_name=u'Коды ОКДП по лицензии')
	sokdps		= models.ManyToManyField(Okdp, through='OrgSOkdp', related_name='sokdp', verbose_name=u'Коды ОКДП по разрешениям')
	phones		= models.ManyToManyField(Phone, through='OrgPhone', verbose_name=u'Телефоны')
	emails		= models.ManyToManyField(Email, through='OrgEmail', verbose_name=u'Адреса жлектропочты')
	events		= models.ManyToManyField(EventType, through='OrgEvent', verbose_name=u'События')	# ? + OKDP? - but OKDP can B blank
	stuffs		= models.ManyToManyField(Person, through='OrgStuff', verbose_name=u'Штат')	# ? + Person
	files		= models.ManyToManyField(File, through='OrgFile', verbose_name=u'Файлы')
	xmlname		= u'orgs'

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name		= u'Организация'
		verbose_name_plural	= u'Организации'

	def	exml(self):
		retvalue = u'\t<org id="%d" name="%s" fullname="%s"' % (self.id, self.name, self.fullname)
		return retvalue + '/>\n'

class	OrgOkved(models.Model):
	org		= models.ForeignKey(Org)
	okved		= models.ForeignKey(Okved)
	xmlname		= u'orgokved'

	class Meta:
		verbose_name		= u'Код ОКВЭД организации'
		verbose_name_plural	= u'Коды ОКВЭД организации'

class	OrgLOkdp(models.Model):
	org		= models.ForeignKey(Org)
	okdp		= models.ForeignKey(Okdp)
	xmlname		= u'orglokdp'

	class Meta:
		verbose_name		= u'Код ОКДП организации по лицензии'
		verbose_name_plural	= u'Коды ОКДП организации по лицензии'

class	OrgSOkdp(models.Model):
	org		= models.ForeignKey(Org)
	okdp		= models.ForeignKey(Okdp)
	xmlname		= u'orgsokdp'

	class Meta:
		verbose_name		= u'Код ОКДП организации по допускам'
		verbose_name_plural	= u'Коды ОКДП организации по допускам'

class	OrgPhone(models.Model):
	org		= models.ForeignKey(Org)
	phone		= models.ForeignKey(Phone)
	xmlname		= u'orgphone'

	class Meta:
		verbose_name		= u'Телефон организации'
		verbose_name_plural	= u'Телефоны организации'

class	OrgEmail(models.Model):
	org		= models.ForeignKey(Org)
	email		= models.ForeignKey(Email)
	xmlname		= u'orgemail'

	class Meta:
		verbose_name		= u'Адрес электропочты организации'
		verbose_name_plural	= u'Адреса электропочты организаций'

class	OrgEvent(models.Model):
	org		= models.ForeignKey(Org)
	type		= models.ForeignKey(EventType)
	okdp		= models.ForeignKey(Okdp, null=True)
	date		= models.DateField(blank=False)
	comments	= models.CharField(max_length=100, blank=True)
	xmlname		= u'orgevent'

	class Meta:
		verbose_name		= u'Событие организации'
		verbose_name_plural	= u'События организаций'

class	OrgStuff(models.Model):
	org		= models.ForeignKey(Org)
	role		= models.ForeignKey(Role)
	person		= models.ForeignKey(Person)
	leader		= models.BooleanField(verbose_name=u'Начальство')
	xmlname		= u'orgstuff'

	def	__unicode__(self):
		return u'%s: %s' % (self.role.name, self.person)

	class Meta:
		verbose_name		= u'Должностное лицо организации'
		verbose_name_plural	= u'Должностные лица организаций'

class	OrgFile(models.Model):
	org		= models.ForeignKey(Org)
	file		= models.ForeignKey(File)
	xmlname		= u'orgfile'

	class Meta:
		verbose_name		= u'Файл организации'
		verbose_name_plural	= u'Файлы организаций'

class	Meeting(models.Model):
	date		= models.DateField(blank=False, verbose_name=u'Дата')
	agenda		= models.CharField(max_length=100, blank=False, verbose_name=u'Повестка')
	log		= models.TextField(blank=True, verbose_name=u'Протокол')
	orgs		= models.ManyToManyField(Org, through='MeetingOrg')
	xmlname		= u'meeting'

	def	__unicode__(self):
		return u'%s %s' % (self.date, self.agenda)

	class Meta:
		ordering = ['date']
		verbose_name		= u'Заседание'
		verbose_name_plural	= u'Заседания'

class	MeetingOrg(models.Model):
	meeting		= models.ForeignKey(Meeting)
	org		= models.ForeignKey(Org)
	xmlname		= u'meetingorg'
