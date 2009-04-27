# -*- coding: utf-8 -*-
from django.db import models

class	Okopf(models.Model):
	'''
	id - by OKOPF, short int
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True)
	name		= models.CharField(max_length=100, blank=False, unique=True)
	shortname	= models.CharField(max_length=10, blank=False, unique=True)
	disabled	= models.BooleanField(blank=False)

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['id']

class	Okved(models.Model):
	'''
	id - by OKVED, str
	'''
	id		= models.CharField(primary_key=True, max_length=6)
	name		= models.CharField(max_length=255, blank=False, unique=True)
	disabled	= models.BooleanField(blank=False)

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['id']

class	Okdp(models.Model):
	'''
	id - by OKDP, int
	'''
	id		= models.PositiveIntegerField(primary_key=True)
	name		= models.CharField(max_length=255, blank=False, unique=True)

	def	__unicode__(self):
		return self.descr

	class Meta:
		ordering = ['id']

class	Okso(models.Model):
	'''
	id - by OKSO, int
	'''
	id		= models.PositiveIntegerField(primary_key=True)
	name		= models.CharField(max_length=255, blank=False, unique=True)
	disabled	= models.BooleanField(blank=False)

	def	__unicode__(self):
		return self.descr

	class Meta:
		ordering = ['id']

class	Qualification(models.Model):
	'''
	id - by OKSO+qualificationid
	'''
	id		= models.PositiveIntegerField(primary_key=True)
	okso		= models.ForeignKey(Okso, blank=False)
	qid		= models.PositiveSmallIntegerField(blank=False)
	name		= models.CharField(max_length=50, blank=False)

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['id']

class	OkdpGroup(models.Model):
	name		= models.CharField(max_length=255, blank=False, unique=True)
	hq		= models.PositiveSmallIntegerField(blank=False)	# highschool specialists qty
	hs		= models.PositiveSmallIntegerField(blank=False)	# highschool specialists seniority
	mq		= models.PositiveSmallIntegerField(blank=False)	# midschool specialists qty
	ms		= models.PositiveSmallIntegerField(blank=False)	# midchool specialists seniority
	oksos		= models.ManyToManyField(Okso, blank=True)

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['id']

class	Okdp4SRO(models.Model):
	id		= models.OneToOneField(Okdp, primary_key=True)
	group		= models.ForeignKey(OkdpGroup, blank=False)

	def	__unicode__(self):
		return self.id.name

	class Meta:
		ordering = ['id']

class	Phone(models.Model):
	country		= models.PositiveIntegerField(blank=False)
	trunk		= models.PositiveIntegerField(blank=False)
	phone		= models.DecimalField(blank=False, max_digits=7, decimal_places=0)
	ext		= models.DecimalField(blank=True, max_digits=4, decimal_places=0)

	def	__unicode__(self):
		if (ext):
			e = u' #%d' % self.ext
		else:
			e = ''
		return u'+%d %d %s%s' % (self.country, self.trunk, self.phone, ext)

	class Meta:
		ordering = ['id']

class	Email(models.Model):
	URL		= models.EmailField(blank=False, unique=True)

class	File(models.Model):
	name		= models.CharField(max_length=255, blank=False)
	mime		= models.CharField(max_length=255, blank=False)
	saved		= models.DateTimeField(blank=False)
	comments	= models.CharField(max_length=255, blank=True)

class	EventType(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True)
	comments	= models.CharField(max_length=100, blank=True)

class	Meeting(models.Model):
	date		= models.DateField(blank=False)
	agenda		= models.CharField(max_length=100, blank=False)
	log		= models.TextField(blank=True)

class	Role(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True)
	comments	= models.CharField(max_length=100, blank=True)

class	Person(models.Model):
	firstname	= models.CharField(max_length=16, blank=False)
	midname		= models.CharField(max_length=24, blank=True)
	lastname	= models.CharField(max_length=24, blank=False)
	qualifications	= models.ManyToManyField(Qualification)

class	PersonFile(models.Model):
	person		= models.ForeignKey(Person)
	file		= models.OneToOneField(File)

class	Org(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True)
	fullname	= models.CharField(max_length=100, blank=False, unique=True)
	regdate		= models.DateField()
	inn		= models.PositiveIntegerField()
	kpp		= models.PositiveIntegerField()
	ogrn		= models.PositiveIntegerField()
	laddress	= models.CharField(max_length=100, blank=False)
	raddress	= models.CharField(max_length=100, blank=True)
	sroregdate	= models.DateField()
	licno		= models.CharField(max_length=30, blank=True)
	licdue		= models.DateField(blank=True)
	okopf		= models.ForeignKey(Okopf)
	okveds		= models.ManyToManyField(Okved, blank=True)
	licokdps	= models.ManyToManyField(Okdp, blank=True, related_name='lokdp')
	srookdps	= models.ManyToManyField(Okdp, blank=True, related_name='sokdp')
	meetings	= models.ManyToManyField(Meeting, blank=True)
	phones		= models.ManyToManyField(Phone, blank=True)
	emails		= models.ManyToManyField(Email, blank=True)

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']

class	OrgEvent(models.Model):
	org		= models.ForeignKey(Org, blank=False)
	type		= models.ForeignKey(EventType, blank=False)
	okdp		= models.ForeignKey(Okdp, blank=True)
	date		= models.DateField(blank=False)
	comments	= models.CharField(max_length=100, blank=True)

class	OrgStuff(models.Model):
	org		= models.ForeignKey(Org)
	role		= models.ForeignKey(Role)
	person		= models.ForeignKey(Person)
	leader		= models.BooleanField()

	def	__unicode__(self):
		return self.role.name

	class Meta:
		ordering = ['id']

class	OrgFile(models.Model):
	org		= models.ForeignKey(Org)
	file		= models.OneToOneField(File)

	def	__unicode__(self):
		return self.file.name

	class Meta:
		ordering = ['id']
