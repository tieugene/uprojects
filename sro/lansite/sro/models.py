# -*- coding: utf-8 -*-
from django.db import models

class	Okopf(models.Model):
	'''
	id - by OKOPF, short int
	'''
	id		= models.PositiveSmallIntegerField(primary_key=True)
	name		= models.CharField(max_length=100, blank=False, unique=True)
	shortname	= models.CharField(max_length=10, null=True)
	disabled	= models.BooleanField(blank=False)

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['id']

class	Okved(models.Model):
	'''
	id - by OKVED, str
	'''
	id		= models.CharField(max_length=6, primary_key=True)
	name		= models.CharField(max_length=255, blank=False, unique=False)
	disabled	= models.BooleanField(blank=False)

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

class	Okso(models.Model):
	'''
	id - by OKSO, int
	'''
	id		= models.PositiveIntegerField(primary_key=True)
	name		= models.CharField(max_length=255, blank=False, unique=False)
	disabled	= models.BooleanField(blank=False)

	def	__unicode__(self):
		return u'%06d %s' % (self.id, self.name)

	class Meta:
		ordering = ['id']

class	Skill(models.Model):
	'''
	id - by OKSO+qualificationid
	'''
	id		= models.PositiveIntegerField(primary_key=True)
	okso		= models.ForeignKey(Okso)
	skill		= models.PositiveSmallIntegerField(blank=False)
	name		= models.CharField(max_length=50, blank=False)

	def	__unicode__(self):
		return u'%06d%d %s' % (self.okso.id, self.skill, self.name)

	class Meta:
		ordering = ['id']

class	Okdp(models.Model):
	'''
	id - by OKDP, int
	'''
	id		= models.CharField(max_length=7, primary_key=True)
	name		= models.CharField(max_length=255, blank=False, unique=False)

	def	__unicode__(self):
		return u'%7s %s' % (self.id, self.name)

	class Meta:
		ordering = ['id']

class	Stage(models.Model):
	id		= models.PositiveSmallIntegerField(primary_key=True)
	name		= models.CharField(max_length=255, blank=False, unique=True)
	hq		= models.PositiveSmallIntegerField(null=True)	# highschool specialists qty
	hs		= models.PositiveSmallIntegerField(null=True)	# highschool specialists seniority
	mq		= models.PositiveSmallIntegerField(null=True)	# midschool specialists qty
	ms		= models.PositiveSmallIntegerField(null=True)	# midchool specialists seniority
	oksos		= models.ManyToManyField(Okso, through='StageOkso')
	okdps		= models.ManyToManyField(Okdp, through='StageOkdp')

	def	__unicode__(self):
		return u'%02d %s' % (self.id, self.name)

	class Meta:
		ordering = ['id']

class	StageOkdp(models.Model):
	id		= models.PositiveIntegerField(primary_key=True)
	stage		= models.ForeignKey(Stage)
	okdp		= models.ForeignKey(Okdp)

class	StageOkso(models.Model):
	id		= models.PositiveIntegerField(primary_key=True)
	stage		= models.ForeignKey(Stage)
	okso		= models.ForeignKey(Okso)

class	Phone(models.Model):
	country		= models.PositiveIntegerField(blank=False)
	trunk		= models.PositiveIntegerField(blank=False)
	phone		= models.DecimalField(max_digits=7, decimal_places=0, blank=False)
	ext		= models.DecimalField(max_digits=4, decimal_places=0, null=True)

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

	def	__unicode__(self):
		return self.URL

class	File(models.Model):
	name		= models.CharField(max_length=255, blank=False)
	mime		= models.CharField(max_length=255, blank=False)
	saved		= models.DateTimeField(blank=False)
	comments	= models.CharField(max_length=255, blank=True)

class	EventType(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True)
	comments	= models.CharField(max_length=100, blank=True)

	def	__unicode__(self):
		return self.name


class	Role(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True)
	comments	= models.CharField(max_length=100, blank=True)

	def	__unicode__(self):
		return self.name

class	Person(models.Model):
	firstname	= models.CharField(max_length=16, blank=False)
	midname		= models.CharField(max_length=24, blank=True)
	lastname	= models.CharField(max_length=24, blank=False)
	skills		= models.ManyToManyField(Skill, through='PersonSkill')

	def	__unicode__(self):
		return u'%s %s %s' % (self.lastname, self.firstname, self.midname)

class	PersonSkill(models.Model):
	person		= models.ForeignKey(Person)
	skill		= models.ForeignKey(Skill)

class	PersonFile(models.Model):
	person		= models.ForeignKey(Person)
	file		= models.OneToOneField(File)

class	Org(models.Model):
	name		= models.CharField(max_length=40, blank=False, unique=True)
	fullname	= models.CharField(max_length=100, blank=False, unique=False)
	regdate		= models.DateField()
	inn		= models.PositiveIntegerField()
	kpp		= models.PositiveIntegerField()
	ogrn		= models.PositiveIntegerField()
	laddress	= models.CharField(max_length=100, blank=False)
	raddress	= models.CharField(max_length=100, null=True)
	sroregdate	= models.DateField()
	licno		= models.CharField(max_length=30, null=True)
	licdue		= models.DateField(, null=True)
	okopf		= models.ForeignKey(Okopf)
	okveds		= models.ManyToManyField(Okved, through='OrgOkved')
	lokdps		= models.ManyToManyField(Okdp, through='OrgLOkdp', related_name='lokdp')
	sokdps		= models.ManyToManyField(Okdp, through='OrgSOkdp', related_name='sokdp')
	phones		= models.ManyToManyField(Phone, through='OrgPhone')
	emails		= models.ManyToManyField(Email, through='OrgEmail')
	events		= models.ManyToManyField(EventType, through='OrgEvent')	# ? + OKDP? - but OKDP can B blank
	stuffs		= models.ManyToManyField(Person, through='OrgStuff')	# ? + Person

	def	__unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']

class	OrgOkved(models.Model):
	org		= models.ForeignKey(Org)
	okved		= models.ForeignKey(Okved)

class	OrgLOkdp(models.Model):
	org		= models.ForeignKey(Org)
	okdp		= models.ForeignKey(Okdp)

class	OrgSOkdp(models.Model):
	org		= models.ForeignKey(Org)
	okdp		= models.ForeignKey(Okdp)

class	OrgPhone(models.Model):
	org		= models.ForeignKey(Org)
	phone		= models.ForeignKey(Phone)

class	OrgEmail(models.Model):
	org		= models.ForeignKey(Org)
	email		= models.ForeignKey(Email)

class	OrgEvent(models.Model):
	org		= models.ForeignKey(Org)
	type		= models.ForeignKey(EventType)
	okdp		= models.ForeignKey(Okdp, null=True)
	date		= models.DateField(blank=False)
	comments	= models.CharField(max_length=100, blank=True)

class	OrgStuff(models.Model):
	org		= models.ForeignKey(Org)
	role		= models.ForeignKey(Role)
	person		= models.ForeignKey(Person)
	leader		= models.BooleanField()

	def	__unicode__(self):
		return self.role.name

class	OrgFile(models.Model):
	org		= models.ForeignKey(Org)
	file		= models.OneToOneField(File)

	def	__unicode__(self):
		return self.file.name

class	Meeting(models.Model):
	date		= models.DateField(blank=False)
	agenda		= models.CharField(max_length=100, blank=False)
	log		= models.TextField(blank=True)
	orgs		= models.ManyToManyField(Org, through='MeetingOrg')

class	MeetingOrg(models.Model):
	meeting		= models.ForeignKey(Meeting)
	org		= models.ForeignKey(Org)

