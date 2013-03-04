#!/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web

web.config.debug = False
render = web.template.render('templates/', cache=False)
message = ""
fullpathre = re.compile(r'^\\\\(\w+)\\(\w+)\\(.*)')
userlist = []
dblist = []
root = ""
mainmenu = render.menu(root)
if os.path.exists('run1s.db'):
	mydb = web.database(dbn='sqlite', db='run1s.db')
else:
	mydb = web.database(dbn='sqlite', db='run1s.db')
	f = open('run1s.sql')
	for i in f:
		mydb.query(i)

# <db>/<action>/[<id>]
# db := user, dbtype, org, db, acl
# action := list, add, del, edit, apply
urls = (
	'/serial', 'serial',
	'/baselist&login=(\w+)&password=(.*)', 'baselist',
	'/', 'index',
	'/export/', 'export',
	'/(\w+)/list/', 'list',
	'/(\w+)/add/', 'add',
	'/(\w+)/del/(\d+)', 'delete',
	'/(\w+)/edit/(\d+)', 'edit',
	'/(\w+)/acl/(\d+)', 'acl'
)

mydict = {
	'user' : {
		"title": "Users:",
		"entry": "User",
		"th": ["Id", "Login", "Password", "Comments"],
		"td": ["id", "login", "password", "comments"]
	},
	'dbtype' : {
		"title": "Database types:",
		"entry": "Database type",
		"th": ["Id", "Name", "Comments"],
		"td": ["id", "name", "comments"]
	},
	'org' : {
		"title": "Organizations:",
		"entry": "Organization",
		"th": ["Id", "Name", "Comments"],
		"td": ["id", "name", "comments"]
	},
	'db' : {
		"title": "Databases:",
		"entry": "Database",
		"th": ["Id", "Organization", "Type", "Comments", "Host", "Share", "Path"],
		"td": ["id", "orgname", "dbtypename", "comments", "hostname", "sharename", "path"]
	}
}

def	countexists(t, w):
	'''
	Search for value in table
	@param
	@return bool
	'''
	return (mydb.query('SELECT COUNT (*) AS total FROM %s WHERE %s' % (t, w))[0].total)

def	exists(t, w):
	'''
	Search for value in table
	@param
	@return bool
	'''
	return (countexists(t, w) > 0)

class	serial:
	def	GET(self):
		return render.baselist(mydb.select('var', where="name='serial'")[0].value)

class	baselist:
	def	GET(self, login, password):
		sn = mydb.select('var', where="name='serial'")[0].value
		if (not exists("user", "login=\"%s\"" % login)):
			retvalue = render.baselist(sn, error = "user not found")
		else:
			a = mydb.select('user', where="login='%s'" % login)[0]
			if (a.password != password):
				retvalue = render.baselist(sn, error = "wrong password")
			else:
				b = mydb.select('baselist', where="userid='%s'" % a.id)
				web.header('Content-Type', 'text/xml')
				retvalue = render.baselist(sn, b)
		return retvalue

class	index:
	def	GET(self):
		return render.index(mainmenu)

class	list:
	'''
	Template args: title, table header, table columns, add form, dbname
	'''
	def	GET(self, dbname):
		global message, mydict
		if message:
			msg = message[:]
			message = ""
		else:
			msg = ""
		if (dbname == 'user'):
			items = mydb.select(dbname, order="login")
			subform = render.useradd()
			acl = True
		elif (dbname in ("dbtype", "org")):
			items = mydb.select(dbname, order="name")
			subform = render.otheradd()
			acl = False
		elif (dbname == 'db'):	# db
			items = mydb.select('dblist', order="orgname, dbtypename, path")
			subform = render.dbadd(mydb)
			acl = True
		else:
			print >> sys.stderr, "Bad page"
		return render.list(root, items, dbname, mydict[dbname], subform, mainmenu, acl, msg)

class	add:
	def	POST(self, dbname):
		'''
		TODO: check on empty, uniq
		'''
		global message, mydict
		i = web.input()
		message = ""
		if (dbname == 'user'):
			i.login = i.login.strip()
			if (i.login == ""):
				message = "Login can't be empty."
			else:
				if (exists("user", "login=\"%s\"" % i.login)):
					message = "Same login already exists."
				else:
					t = mydb.transaction()
					try:
						mydb.insert(dbname, login=i.login, password=i.password, comments=i.comments)
					except:
						t.rollback()
						message = 'Error adding. Call sysadmin'
					else:
						t.commit()
		elif (dbname in ("dbtype", "org")):
			i.name = i.name.strip()
			if (i.name == ""):
				message = "Name can't be empty."
			else:
				if (exists(dbname, "name=\"%s\"" % i.name)):
					message = "Same name already exists."
				else:
					t = mydb.transaction()
					try:
						mydb.insert(dbname, name=i.name, comments=i.comments)
					except:
						t.rollback()
						message = 'Error adding. Call sysadmin'
					else:
						t.commit()
		else:	# db
			if not fullpathre.match(i.fullpath):
				message = "Path must be in form: \\\\<host>\\<share>\\<path>"
			else:
				host, share, path = fullpathre.split(i.fullpath.lower())[1:4]
				# cascade insert.
				t = mydb.transaction()
				try:
					# 1. Host
					count = exists("host", "name=\"%s\"" % host)
					if (not count):
						hostid = mydb.insert("host", name=host)
					else:
						hostid = int(mydb.select('host', where='name="%s"' % host)[0].id)
						count = exists("share", "hostid=\"%d\" AND name=\"%s\"" % (hostid, share))
					# 2. Share
					if (not count):
						shareid = mydb.insert('share', name=share, hostid=hostid)
					else:
						shareid = int(mydb.select('share', where='hostid="%d" AND name="%s"' % (hostid, share))[0].id)
						count = exists("db", "shareid=\"%d\" AND path=\"%s\"" % (shareid, path))
					# 3. DB
					if (not count):
						id = mydb.insert('db', path=path, shareid=shareid, dbtypeid=int(i.dbtype), orgid=int(i.org), comments=i.comments)
					else:
						message = "Database already exists"
				except:
					t.rollback()
					message = 'Error db. Call sysadmin'
				else:
					t.commit()
		raise web.seeother("/%s/list/" % dbname)

class	delete:
	def	GET(self, dbname, id):
		global message, fullpathre
		if (dbname == 'db'):	# cascade up deletion of shares and servers
			id = int(id)
			item = mydb.select(dbname, where="id=%d" % id)[0]
			shareid = int(item.shareid)
			count = countexists("db", "shareid=%d" % shareid)
			t = mydb.transaction()
			try:
				mydb.delete(dbname, where="id=%d" % id)	# option
				if (count == 1):	# check on orphan share
					item = mydb.select('share', where="id=%d" % shareid)[0]
					hostid = int(item.hostid)
					count = countexists("share", "hostid=%d" % hostid)
					mydb.delete('share', where="id=%d" % shareid)	# option
					if (count == 1):	# check on orphan server
						mydb.delete('host', where="id=%d" % hostid)
			except:
				t.rollback()
				message = "Error deleting %s. Call sysadmin" % dbname
			else:
				t.commit()
		else:
			t = mydb.transaction()
			try:
				mydb.delete(dbname, where="id=%d" % int(id))
			except:
				t.rollback()
				message = "Error deleting %s. Call sysadmin" % dbname
			else:
				t.commit()
		raise web.seeother("/%s/list/" % dbname)

class	edit:
	def	GET(self, dbname, id):
		global message, mydict
		id = int(id)
		item = mydb.select(dbname, where="id = %d" % id)[0]
		if (dbname == 'user'):
			retvalue = render.useredit(root, item, mainmenu)
		elif (dbname in ("dbtype", "org")):
			retvalue = render.otheredit(root, dbname, mydict[dbname]['entry'], item, mainmenu)
		elif (dbname == 'db'):	# db
			retvalue = render.dbedit(root, mydb, item, mainmenu)
		else:
			print >> sys.stderr, "Bad page"
			retvalue = render.index(root)
		return retvalue
	def	POST(self, dbname, id):
		global message, mydict
		id = int(id)
		i = web.input()
		nextform = "list"
		if (dbname == 'user'):
			i.login = i.login.strip()
			if (i.login == ""):
				message = "Login can't be empty."
				nextform = "edit"
			else:
				if exists("user", "id<>%d AND login=\"%s\"" % (id, i.login)):
					message = "Same login already exists."
					nextform = "edit"
				else:
					t = mydb.transaction()
					try:
						mydb.update(dbname, where="id = %d" % id, login = i.login, password = i.password, comments = i.comments)
					except:
						t.rollback()
						message = "Error deleting %s. Call sysadmin" % dbname
					else:
						t.commit()
		elif (dbname in ("dbtype", "org")):
			i.name = i.name.strip()
			if (i.name == ""):
				message = "Name can't be empty."
				nextform = "edit"
			else:
				if exists(dbname, "id<>%d AND name=\"%s\"" % (id, i.name)):
					message = "Same name already exists."
					nextform = "edit"
				else:
					t = mydb.transaction()
					try:
						mydb.update(dbname, where="id = %d" % id, name = i.name, comments = i.comments)
					except:
						t.rollback()
						message = "Error deleting %s. Call sysadmin" % dbname
					else:
						t.commit()
		else:	# db
			i.path = i.path.strip()
			i.path = i.path.strip('/')
			t = mydb.transaction()
			try:
				mydb.update('db', where="id = %d" % id, shareid = int(i.shareid), dbtypeid = int(i.dbtypeid), orgid = int(i.orgid), path = i.path, comments = i.comments)
			except:
				t.rollback()
				message = "Error deleting %s. Call sysadmin" % dbname
			else:
				t.commit()
		raise web.seeother("/%s/%s/" % (dbname, nextform))

class	acl:
	def	GET(self, dbname, id):
		global userlist, dblist
		id = int(id)
		if (dbname == "user"):
			item = mydb.select(dbname, where="id = %d" % id)[0]
			retvalue = render.useracl(root, item, mydb, mainmenu)
		else:	# db
			item = mydb.select("dblist", where="id = %d" % id)[0]
			retvalue = render.dbacl(root, item, mydb, mainmenu)
		return retvalue
	def	POST(self, dbname, id):
		global userlist, dblist
		i = web.input()
		t = mydb.transaction()
		try:
			if (dbname == "user"):
				mydb.delete('acl', where="userid=%d" % int(id))
				for k in i.keys():
					mydb.insert('acl', dbid=int(k), userid=int(id), visible=True)
			else:	# db
				mydb.delete('acl', where="dbid=%d" % int(id))
				for k in i.keys():
					mydb.insert('acl', dbid=int(id), userid=int(k), visible=True)
		except:
			t.rollback()
			message = "Error refreshing ACL. Call sysadmin"
		else:
			t.commit()
		raise web.seeother("/%s/list/" % dbname)

class	export:
	def	GET(self):
		text = ""
		for i in mydb.select("user", where="1=1"):
			text += "user\t%d\t%s\t%s\t%s\n" % (i.id, i.login, i.password, i.comments)
		for i in mydb.select("org", where="1=1"):
			text += "org\t%d\t%s\t%s\n" % (i.id, i.name, i.comments)
		for i in mydb.select("dbtype", where="1=1"):
			text += "dbtype\t%d\t%s\t%s\n" % (i.id, i.name, i.comments)
		for i in mydb.select("host", where="1=1"):
			text += "host\t%d\t%s\t%s\n" % (i.id, i.name, i.comments)
		for i in mydb.select("share", where="1=1"):
			text += "share\t%d\t%d\t%s\t%s\n" % (i.id, i.hostid, i.name, i.comments)
		for i in mydb.select("db", where="1=1"):
			text += "db\t%d\t%d\t%d\t%d\t%s\t%s\n" % (i.id, i.shareid, i.dbtypeid, i.orgid, i.path, i.comments)
		for i in mydb.select("acl", where="1=1"):
			text += "acl\t%d\t%d\t%d\n" % (i.id, i.userid, i.dbid)
		web.header("Content-Type", "text/plain;")
		web.header("Content-Transfer-Encoding", "binary");
		web.header("Content-Disposition", "attachment; filename=\"run1s.txt\";");
		#web.header("Content-Length", "%d" % len(text));
		return text

if __name__ == "__main__":
	web.application(urls, globals()).run()
else:
	root = "/run1s"
	mainmenu = render.menu(root)
	application = web.application(urls, globals()).wsgifunc()
