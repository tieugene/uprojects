# -*- coding: utf-8 -*-
'''
Software
from xdg import Mime
import mimetypes
Mime.get_type(<filename>)	# > .media, .subtype
a = Mime.lookup('application/vnd.ms-excel')
a.get_comments()
? Mime.exts
'''

from __future__ import with_statement
from xdg import Mime
import sys, os, re, hashlib, tempfile
import web
import var, config

class	MimeHelper:
	'''
	Class to help process mimetypes.
	MIMEtype: .media, .subtype, ._comments (need load)
	'''
	def	__init__(self):
		self.type2ext = {}
		self.loaded = False
	def	gettype(self, f):
		'''
		@param f:file - file
		@return Mime.MIMEtype
		'''
		return Mime.get_type(f)
	def	getext(self, mime):
		'''
		@param mime:MIMEtype
		@return list of exts
		'''
		if (not self.loaded):		# fill dict after first call of get_*
			for e in Mime.exts.keys():	# e = extension:str
				t = Mime.exts[e]	# t = MIMEtype
				if not t in self.type2ext:
					self.type2ext[t] = []
				self.type2ext[t].append(e)
		return self.type2ext[mime]

mimehelper	= MimeHelper()

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
			ext = var.mydb.select('file', where='id=%s' % id)[0].ext
			t = var.mydb.transaction()
			try:
				n = var.mydb.delete('object', where='id=%s' % id)
			except:
				t.rollback()
				var.message = 'Error deleting programm'
				success = False
			else:
				t.commit()
				var.message = '%d programm deleted ok' % n
				success = True
			if (success):
				filename = os.path.join(config.filepath, "%08X.%s" % (int(id), ext))
				os.remove(filename)
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
		'''
		list, None: adding
		edit, <id>: editing
		To add:
			1. get file
			2. get tmp ext (or none => unknown file type?)
			3. try write tmp file
		'''
		raiseform = self.mainlistname
		if (view == 'list'):
			# 1. get file, get hash
			x = web.input(myfile={})['myfile']
			newmd5 = hashlib.md5(x.value).hexdigest()
			# 3. write temporary as is
			#f = tmpfile.NamedTemporaryFile(mode="wb", suffix=tmpext[0], dir=config.filepath, delete=False)
			tmpfn = os.path.join(config.tmppath, x.filename)
			with open(tmpfn, "wb") as f:
				f.write(x.value)
			# 4. get mime, extension, hash
			newmimetype = Mime.get_type(tmpfn)
			tmpext = mimehelper.getext(newmimetype)
			newext = tmpext[0] if tmpext else ""
			# 5. try add record to object => id
			t = var.mydb.transaction()
			try:
				newid = var.mydb.insert('object')
				# 6. mk filename ("%08X" % id)
				newfn = "%08X" % newid
				var.mydb.insert('file',
					id = newid,
					size = os.path.getsize(tmpfn),
					md5 = newmd5,
					mimetype = "%s/%s" % (newmimetype.media, newmimetype.subtype),
					origfn = x.filename,
					ext = newext)
				var.mydb.insert(self.dbname,
					id = newid)
				# 7. try rename file
				os.rename(tmpfn, os.path.join(config.filepath, newfn + "." + newext))
			except:
				t.rollback()
				os.remove(tmpfn)
				var.message = 'Error inserting programm'
			else:
				t.commit()
				raiseform = "/soft/main/edit/%d" % newid
		elif (view == 'edit'):
			i = web.input()
			t = var.mydb.transaction()
			try:
				var.mydb.update(self.dbname, where="id=%s" % id,
					platform=int(i.platform),
					vendor=int(i.vendor),
					distrib=int(i.distrib),
					name=i.name,
					ver=i.ver)
				var.mydb.update('file', where="id=%s" % id,
					mimetype=i.mimetype,
					origfn=i.origfn)
				var.mydb.update('object', where="id=%s" % id,
					comments=i.comments)
			except:
				t.rollback()
				var.message = 'Error updating programm'
			else:
				t.commit()
		raise web.seeother(raiseform)

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
