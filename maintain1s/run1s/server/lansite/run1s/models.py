# -*- coding: utf-8 -*-
from django.db import models

class	Var(models.Model):
	name = models.CharField(max_length=10, blank=False, unique=True, db_index=True)
	value = models.IntegerField(default=0)

	def	__unicode__(self):
		return self.name

class	Org(models.Model):
	name = models.CharField(max_length=40, blank=False, unique=True)
	comments = models.CharField(max_length=100, blank=True)

	def	__unicode__(self):
		return self.name

class	Dbtype(models.Model):
	name = models.CharField(max_length=50, blank=False, unique=True)
	comments = models.CharField(max_length=100, blank=True)

	def	__unicode__(self):
		return self.name

class	Host(models.Model):
	name = models.CharField(max_length=20, blank=False, unique=True)
	comments = models.CharField(max_length=100, blank=True)

	def	__unicode__(self):
		return self.name

class	Share(models.Model):
	host = models.ForeignKey(Host)
	name = models.CharField(max_length=50, blank=False, db_index=True)
	comments = models.CharField(max_length=100, blank=True)

	def	__unicode__(self):
		return u'\\\\%s\\%s' % (self.host, self.name)

class	Db(models.Model):
	org = models.ForeignKey(Org)
	type = models.ForeignKey(Dbtype)
	share = models.ForeignKey(Share)
	path = models.CharField(max_length=100, db_index=True, blank=True)
	comments = models.CharField(max_length=100, blank=True)

	def	__unicode__(self):
		return u'%s\\%s' % (self.share, self.path)

class	User(models.Model):
	login = models.CharField(max_length=20, blank=False, unique=True)
	password = models.CharField(max_length=20, blank=False)
	comments = models.CharField(max_length=100, blank=True)
	dbs = models.ManyToManyField(Db, blank=True)

	def	__unicode__(self):
		return self.login
