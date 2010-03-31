# -*- coding: utf-8 -*-

'''
Multitask: subtasks w/o subj, desk, etc - just assignee, state
'''

from django.db import models
from django.contrib.auth.models import User
from polymorphic import PolymorphicModel
from datetime import datetime

class	GwUser(models.Model):
	user		= models.OneToOneField(User, null=False, blank=False, verbose_name=u'Пользователь')

	def	asstr(self):
		return self.user.username

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering = ('user',)
		verbose_name = u'Пользователь GW'
		verbose_name_plural = u'Пользователи GW'

class	Object(PolymorphicModel):
	'''
	Объект - прародитель всех остальных.
	ancestor - объект, от которого данный объект наследует свойства, не определенные в данном объекте (наследование).
	master	- объект выше по иерархии группировки (включение)
	links	- группы (кластеры) связанных объектов, в который включен данные объект
	'''
	ancestor	= models.ForeignKey('self', null=True, blank=True, related_name='ancestor_set', verbose_name=u'Предок')
	master		= models.ForeignKey('self', null=True, blank=True, related_name='master_set', verbose_name=u'Хозяин')
	#links		= models.ManyToManyField(self, throughnull=True,  blank=True,  unique=False, verbose_name=u'Связи')

	class	Meta:
		verbose_name		= u'Объект'
		verbose_name_plural	= u'Объекты'
'''
class	LinkCluster:
	pass

class	ObjectLink:
	cluster:LinkCluster
	object:Object
	unique_together = ((cluster, object),)
'''
class	AddrShort(models.Model):
	'''
	Сокращение для адреса: ул.=улица etc
	'''
	shortname	= models.CharField(max_length=10, blank=False, unique=True, verbose_name=u'Краткое наименование')
	fullname	= models.CharField(max_length=64, blank=False, unique=True, verbose_name=u'Полное наименование')

	def	__unicode__(self):
		return self.name

	class	Meta:
		ordering		= ('shortname', )
		verbose_name		= u'Сокращение адреса'
		verbose_name_plural	= u'Сокращения адресов'

class	Address(Object):
	'''
	Адрес (РФ) - рекурсивный
	'''
	zip		= models.PositiveIntegerField(null=True, blank=True, verbose_name=u'Индекс')
	name		= models.CharField(max_length=40, null=True, blank=False, verbose_name=u'Наименование')
	type		= models.ForeignKey(AddrShort, null=False, blank=False, verbose_name=u'Сокращение')
	typeplace	= models.SmallIntegerField(null=True, blank=True, verbose_name=u'Расположение типа')
	parent		= models.ForeignKey('self', null=True, blank=True, verbose_name=u'Предок')
	publish		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Печатать')
	endpoint	= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Конец')

	def	__unicode__(self):
		return self.name

	class	Meta:
		verbose_name		= u'Адрес'
		verbose_name_plural	= u'Адреса'

class	Phone(Object):
	'''
	Телефонный номер
	'''
	no		= models.CharField(max_length=15, null=False, blank=False, verbose_name=u'Номер')	# 15 символов - согласно ITU-T E.164

	def	__unicode__(self):
		return self.no

	class	Meta:
		verbose_name		= u'Номер телефона'
		verbose_name_plural	= u'Номера телефонов'

class	PhoneWExt(Phone):
	'''
	Телефонный номер
	'''
	ext		= models.CharField(max_length=4, null=False, blank=False, verbose_name=u'DTMF')

	def	__unicode__(self):
		return u'%s#%s' % (self.no, self.ext)

	class	Meta:
		verbose_name		= u'Номер телефона с донабором'
		verbose_name_plural	= u'Номера телефонов с донабором'

class	Contact(Object):
	addr		= models.ManyToManyField(Address, through='ContactAddr', verbose_name=u'Адреса')
	phone		= models.ManyToManyField(Phone, through='ContactPhone', verbose_name=u'Телефоны')

#	def	__unicode__(self):
#		return self.name

	class	Meta:
		verbose_name		= u'Контакт'
		verbose_name_plural	= u'Контакты'

class	AddrType(models.Model):
	'''
	Тип адреса: Домашний, Юридический, Почтовый, Доставки etc
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=20, blank=False, unique=True, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class	Meta:
		ordering		= ('id', )
		verbose_name		= u'Тип адреса'
		verbose_name_plural	= u'Типы адресов'

class	PhoneType(models.Model):
	'''
	Тип телефона: Сотовый, Фиксированный (PST?), Факс, Модем, Домашний, Личный, Рабочий etc.
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True, verbose_name=u'Код')
	name		= models.CharField(max_length=20, blank=False, unique=True, verbose_name=u'Наименование')

	def	__unicode__(self):
		return self.name

	class	Meta:
		ordering		= ('id', )
		verbose_name		= u'Тип телефона'
		verbose_name_plural	= u'Типы телефонов'

class	ContactAddr(models.Model):
	contact		= models.ForeignKey(Contact,  null=False, blank=False, verbose_name=u'Контакт')
	addr		= models.ForeignKey(Address,  null=False, blank=False, verbose_name=u'Адрес')
	type		= models.ForeignKey(AddrType, null=False, blank=False, verbose_name=u'Тип')

	def	__unicode__(self):
		return u'%s: %s (%s)' % (self.contact, self.addr, self.type)

	class	Meta:
		ordering		= ('contact', 'type', 'addr',)
		unique_together		= (('contact', 'type', 'addr',),)
		verbose_name		= u'Контакт.Адрес'
		verbose_name_plural	= u'Контакты.Адреса'

class	ContactPhone(models.Model):
	contact		= models.ForeignKey(Contact,  null=False, blank=False, verbose_name=u'Контакт')
	phone		= models.ForeignKey(Phone,  null=False, blank=False, verbose_name=u'Телефон')
	type		= models.ForeignKey(PhoneType, null=False, blank=False, verbose_name=u'Тип')

	def	__unicode__(self):
		return u'%s: %s (%s)' % (self.contact, self.phone, self.type)

	class	Meta:
		ordering		= ('contact', 'phone', 'type',)
		unique_together		= (('contact', 'phone', 'type',),)
		verbose_name		= u'Контакт.Телефон'
		verbose_name_plural	= u'Контакты.Телефоны'

class	Person(Contact):
	firstname	= models.CharField(max_length=16, null=True, blank=True, verbose_name=u'Имя')
	midname		= models.CharField(max_length=24, null=True, blank=True, verbose_name=u'Отчество')
	lastname	= models.CharField(max_length=24, null=True, blank=True, verbose_name=u'Фамилия')
	birthdate	= models.DateField(null=True, blank=True, verbose_name=u'День рождения')
	sex		= models.BooleanField(null=False, blank=False, default=True, verbose_name=u'Пол')

	def	__unicode__(self):
		return self.name

	class	Meta:
		verbose_name		= u'Человек'
		verbose_name_plural	= u'Люди'

class	Org(Contact):
	cn		= models.CharField(max_length=64, null=False, blank=False, unique=True, verbose_name=u'Common name')
	stuffs		= models.ManyToManyField(Person, through='OrgStuff', verbose_name=u'Штат')

	def	__unicode__(self):
		return self.cn

	class	Meta:
		verbose_name = u'Организация'
		verbose_name_plural = u'Организации'

class	JobRole(models.Model):
	name		= models.CharField(max_length=64, blank=False, unique=True, verbose_name=u'Наименование')
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

class	OrgStuff(models.Model):
	org		= models.ForeignKey(Org, verbose_name=u'Организация')
	role		= models.ForeignKey(JobRole, verbose_name=u'Должность')
	person		= models.ForeignKey(Person, verbose_name=u'Человек')

	def	asstr(self):
		return u'%s, %s: %s' % (self.org.asstr(), self.role.asstr(), self.person.asstr())

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		verbose_name		= u'Организация.Должностное лицо'
		verbose_name_plural	= u'Организация.Должностные лица'
		unique_together		= [('org', 'role', 'person')]

class	Org_RU(Org):
	shortname	= models.CharField(max_length=64, null=True, blank=True, verbose_name=u'Краткое наименование')
	fullname	= models.CharField(max_length=128, null=True, blank=True, verbose_name=u'Полное наименование')
	brandname	= models.CharField(max_length=128, null=True, blank=True, verbose_name=u'Фирменное наименование')
	egruldate	= models.DateField(null=True, blank=True, verbose_name=u'Дата регистрации в ЕГРЮЛ')
	inn		= models.CharField(null=True, blank=True, max_length=12, unique=True, verbose_name=u'ИНН')
	kpp		= models.CharField(null=True, blank=True, max_length= 9, verbose_name=u'КПП')
	ogrn		= models.CharField(null=True, blank=True, max_length=15, unique=True, verbose_name=u'ОГРН')

	class	Meta:
		verbose_name = u'Организация (РФ)'
		verbose_name_plural = u'Организации (РФ)'

class	Task(Object):
	author		= models.ForeignKey(GwUser, null=False, blank=False, related_name='author_id', verbose_name=u'Автор')
	created		= models.DateTimeField(null=False, blank=False, default=datetime.now, verbose_name=u'Создана')
	deadline	= models.DateField(null=True, blank=True, verbose_name=u'Завершить до')
	subject		= models.CharField(max_length=128, null=False, blank=False, verbose_name=u'Тема')
	description	= models.TextField(null=True, blank=True, verbose_name=u'Подробности')
	done		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Завершено')

	def	__unicode__(self):
		return self.name

	class	Meta:
		verbose_name = u'Задача'
		verbose_name_plural = u'Задачи'

class	ToDoCat(models.Model):
	name		= models.CharField(max_length=64, null=False, blank=False, unique=True, verbose_name=u'Наименование')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('name',)
		verbose_name		= u'ToDo.Категория'
		verbose_name_plural	= u'ToDo.Категории'

class	ToDo(Task):
	category	= models.ForeignKey(ToDoCat, null=True, blank=True, verbose_name=u'Категория')

	def	__unicode__(self):
		return self.name

	class	Meta:
		verbose_name = u'Задача'
		verbose_name_plural = u'Задачи'

class	AssignCat(models.Model):
	name		= models.CharField(max_length=64, null=False, blank=False, unique=True, verbose_name=u'Наименование')
	description	= models.TextField(null=True, blank=True, verbose_name=u'Подробности')

	def	asstr(self):
		return self.name

	def	__unicode__(self):
		return self.asstr()

	class	Meta:
		ordering		= ('name',)
		verbose_name		= u'Задание.Категория'
		verbose_name_plural	= u'Задания.Категории'

class	Assign(Task):
	'''
	state
	comments
	files
	DependsOn - tasks not sons
	'''
	assignee	= models.ForeignKey(GwUser, null=False, blank=False, related_name='assignee_id', verbose_name=u'Исполнитель')
	importance	= models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'Важность')
	read		= models.BooleanField(null=False, blank=False, default=False, verbose_name=u'Прочтено')
	category	= models.ForeignKey(AssignCat, null=True, blank=True, verbose_name=u'Категория')

	def	__unicode__(self):
		return self.subject

	class	Meta:
		verbose_name = u'Задание'
		verbose_name_plural = u'Задания'

# class	Appointment (iCalendar/Meeting)
# class	Event (iEvent)
