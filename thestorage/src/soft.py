# -*- coding: utf-8 -*-
'''
'''

from __future__ import with_statement
from xdg import Mime
import sys, os, re, hashlib, tempfile
import web
import config, var, common

def	date2tuple(d):
	'''
	Converts date in form of int timestamp into tuple of values.
	Unused values replaced w/ None.
	E.g. 2000 => (2000, None, ...), 200809 => (2008, 9, None, ...) etc
	@param d:int - date
	@return (y, m, d, h, m, s)
	'''
	d_str = str(d)
	year	= int(d_str[:4]) if (d) else None
	month	= int(d_str[4:6]) if (year) and (len(d_str) > 4) else None
	day	= int(d_str[6:8]) if (month) and (len(d_str) > 6) else None
	hour	= int(d_str[8:10]) if (day) and (len(d_str) > 8) else None
	minute	= int(d_str[10:12]) if (hour) and (len(d_str) > 10) else None
	second	= int(d_str[12:14]) if (minute) and (len(d_str) > 12) else None
	return (year, month, day, hour, minute, second)


def	tuple2date(year, month, day, hour, minute, second):
	'''
	Converts date in form of tuple into timestamp as int.
	E.g. (2000, -1, ...) => 2000, (2008, 9, -1, ...) => 200809  etc
	@param (y, m, d, h, m, s)
	@return int
	'''
	datetime = ""
	tmp = "%04d" % year if (year >= 0) else ""
	datetime += tmp
	tmp = "%02d" %  month if (tmp) and (month >= 0) else ""
	datetime += tmp
	tmp = "%02d" % day if (tmp) and (day >= 0) else ""
	datetime += tmp
	tmp = "%02d" % hour if (tmp) and (hour >= 0) else ""
	datetime += tmp
	tmp = "%02d" % minute if (tmp) and (minute >= 0) else ""
	datetime += tmp
	tmp = "%02d" % second if (tmp) and (second >= 0) else ""
	datetime += tmp
	if len(datetime) == 0:
		datetime = None
	return datetime


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
	def	GET(self, view = 'list', id = None):
		if (view == 'list'):
			items = var.mydb.select('softview')
			return self.listform(var.root, items)
		elif (view == 'download'):
			item = var.mydb.select('softview', where='id=%s' % id)[0]
			web.header("Content-Type", "%s/%s;" % (item.mime_media, item.mime_type))
			web.header("Content-Transfer-Encoding" , "binary"); 
			web.header("Content-Disposition", "attachment; filename=\"%s\";" % item.origfn);
			web.header("Content-Length", "%d" % item.size); 
			return open(os.path.join(config.filepath, "%08X" % (int(item.id)))).read()
		elif (view == 'view'):
			item = var.mydb.select('softview', where='id=%s' % id)[0]
			return self.viewform(var.root, item)
		elif (view == 'edit'):
			item = var.mydb.select('softview', where='id=%s' % id)[0]
			return self.editform(var.root, item, var.mydb, date2tuple(item.datetime))
		elif (view == 'del'):
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
				filename = os.path.join(config.filepath, "%08X" % (int(id)))
				os.remove(filename)
			raise web.seeother(self.mainlistname)
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
			mimeid = int(var.mydb.select('mimesubtype', where='name="%s"' % newmimetype.subtype)[0].id) # FIXME: if none
			# 5. try add record to object => id
			t = var.mydb.transaction()
			#if (True):
			try:
				newid = var.mydb.insert('object')
				# 6. mk filename ("%08X" % id)
				newfn = "%08X" % newid
				var.mydb.insert('file',
					id = newid,
					size = os.path.getsize(tmpfn),
					md5 = newmd5,
					mime = mimeid,
					origfn = x.filename)
				var.mydb.insert(self.dbname,
					id = newid)
				# 7. try rename file
				os.rename(tmpfn, os.path.join(config.filepath, newfn))
			except:
				t.rollback()
				os.remove(tmpfn)
				var.message = 'Error inserting programm'
			else:
				t.commit()
				raiseform = "/soft/main/edit/%d" % newid
		elif (view == 'edit'):
			i = web.input()
			dt = tuple2date(int(i.year), int(i.month), int(i.day), int(i.hour), int(i.minute), int(i.second))
			t = var.mydb.transaction()
			try:
				var.mydb.update(self.dbname, where="id=%s" % id,
					platform=int(i.platform),
					vendor=int(i.vendor),
					distrib=int(i.distrib),
					name=i.name,
					ver=i.ver)
				var.mydb.update('file', where="id=%s" % id,
					datetime=dt,
					mime=i.mime,
					origfn=i.origfn)
				var.mydb.update('object', where="id=%s" % id,
					comments=i.comments)
			except:
				t.rollback()
				var.message = 'Error updating programm'
			else:
				t.commit()
		raise web.seeother(raiseform)

class	vendor(common.ref):
	def	__init__(self):
		ref.__init__(self, 'vendor', '/soft/vendor/list/')
	def	GET(self, view, id = None):
		return ref.GET(self, view, id)
	def	POST(self, view, id = None):
		return ref.POST(self, view, id)

class	distrib(common.ref):
	def	__init__(self):
		ref.__init__(self, 'distrib', '/soft/distrib/list/')
	def	GET(self, view, id = None):
		return ref.GET(self, view, id)
	def	POST(self, view, id = None):
		return ref.POST(self, view, id)

class	platform(common.ref):
	def	__init__(self):
		ref.__init__(self, 'platform', '/soft/platform/list/')
	def	GET(self, view, id = None):
		return ref.GET(self, view, id)
	def	POST(self, view, id = None):
		return ref.POST(self, view, id)

class	settings:
	def	GET(self, action):
		return var.render.soft_settings()
