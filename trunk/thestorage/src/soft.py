# -*- coding: utf-8 -*-
'''
Software
from xdg import Mime
Mime.get_type(<filename>)
a = Mime.lookup('application/vnd.ms-excel')
a.get_comments()
'''

from __future__ import with_statement
import sys, os, re, hashlib
import web
import var

def	CheckUniq(db, wh):
		count = False
		for i in var.mydb.select(db, where=wh):
			count = True
			break
		return count

def	GetMsg():
	if (var.message):
		msg = var.message[:]
		var.message = None
	else:
		msg = None
	return msg

class	menu:
	def	GET(self):
		return var.render.soft_menu(var.root)

class	main:
	def	__init__(self):
		self.dbname = 'programm'
		self.mainlistname = '/soft/main/list/'
		self.listform = var.render.soft_list
		self.viewform = var.render.soft_view
		self.editform = var.render.soft_edit
	def	GET(self, view, id = None):
		if (view == 'list'):
			items = var.mydb.select('softview')
			return self.listform(var.root, items)
		elif (view == 'del'):
			t = var.mydb.transaction()
			try:
				n = var.mydb.delete(self.dbname, where='id=%s' % id)
			except:
				t.rollback()
				var.message = 'Error deleting programm'
			else:
				t.commit()
				var.message = '%d programm deleted ok' % n
			raise web.seeother(self.mainlistname)
		elif (view == 'view'):
			item = var.mydb.select('softview', where='id=%s' % id)[0]
			return self.viewform(var.root, item)
		elif (view == 'edit'):
			item = var.mydb.select('softview', where='id=%s' % id)[0]
			platform = var.mydb.select('platform')
			vendor = var.mydb.select('vendor')
			distrib = var.mydb.select('distrib')
			return self.editform(var.root, item, platform, vendor, distrib)
		else:
			var.message = 'Unknown action'
			raise web.seeother(self.mainlistname)
	def	POST(self, view, id = None):
		x = web.input(myfile={})['myfile']
		with open(os.path.join(config.filepath, x.filename), "wb") as f:
			f.write(x.value)
			print hashlib.md5(x.value).hexdigest()
		raise web.seeother(self.mainlistname)

class	ref:
	'''
	Common parent for siple references: id, name, comments
	'''
	def	__init__(self, dbname, mainlistname):
		self.dbname = dbname
		self.mainlistname = mainlistname
		self.listform = var.render.ref_list
		self.editform = var.render.ref_edit
	def	GET(self, view, id = None):
		if (view == 'list'):
			items = var.mydb.select(self.dbname)
			return self.listform(var.root, items, self.dbname, GetMsg())
		elif (view == 'del'):
			t = var.mydb.transaction()
			try:
				n = var.mydb.delete(self.dbname, where='id=%s' % id)
			except:
				t.rollback()
				var.message = 'Error deleting %s' % self.dbname
			else:
				t.commit()
				var.message = '%d %s deleted ok' % (n, self.dbname)
			raise web.seeother(self.mainlistname)
		elif (view == 'edit'):
			item = var.mydb.select(self.dbname, where='id=%s' % id)[0]
			return self.editform(var.root, item, self.dbname, GetMsg())
		else:
			var.message = 'Unknown action'
			raise web.seeother(self.mainlistname)
	def	POST(self, view, id = None):	# list, None | edit, 2
		i = web.input()			# name, comments
		if (view == 'list'):
			if CheckUniq(self.dbname, 'name="%s"' % i.name):
				var.message = "%s w/ same name already exists." % self.dbname
			else:
				t = var.mydb.transaction()
				try:
					n = var.mydb.insert(self.dbname, name=i.name, comments=i.comments)
				except:
					t.rollback()
					var.message = 'Error inserting %s' % self.dbname
				else:
					t.commit()
					var.message = '%d %s added ok' % (n, self.dbname)
		elif (view == 'edit'):
			t = var.mydb.transaction()
			try:
				var.mydb.update(self.dbname, where="id=%s" % id, name=i.name, comments=i.comments)
			except:
				t.rollback()
				var.message = 'Error updating %s' % self.dbname
			else:
				t.commit()
		raise web.seeother(self.mainlistname)

class	vendor(ref):
	def	__init__(self):
		ref.__init__(self, 'vendor', '/soft/vendor/list/')
	def	GET(self, view, id = None):
		return ref.GET(self, view, id)
	def	POST(self, view, id = None):
		return ref.POST(self, view, id)

class	distrib(ref):
	def	__init__(self):
		ref.__init__(self, 'distrib', '/soft/distrib/list/')
	def	GET(self, view, id = None):
		return ref.GET(self, view, id)
	def	POST(self, view, id = None):
		return ref.POST(self, view, id)

class	platform(ref):
	def	__init__(self):
		ref.__init__(self, 'platform', '/soft/platform/list/')
	def	GET(self, view, id = None):
		return ref.GET(self, view, id)
	def	POST(self, view, id = None):
		return ref.POST(self, view, id)

class	settings:
	def	GET(self, action):
		pass
