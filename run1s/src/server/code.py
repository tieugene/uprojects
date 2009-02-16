#!/bin/env python
'''
TODO: transactions, triggers
'''
import web, re, pprint

web.config.debug = False
render = web.template.render('templates/', cache=False)	#"templates/"
mydb = web.database(dbn='sqlite', db='run1s.db')
message = ""
fullpathre = re.compile(r'^\\\\(\w+)\\(\w+)\\(.*)')
userlist = []
dblist = []

# <db>/<action>/[<id>]
# db := user, dbtype, org, db, acl
# action := list, add, del, edit, apply
urls = (
	'/', 'index',
	'/menu', 'menu',
	'/acl', 'acl',
	'/serial', 'serial',
	'/baselist&login=(\w+)&password=(.*)', 'baselist',
	'/(\w+)/list/', 'list',
	'/(\w+)/add/', 'add',
	'/(\w+)/del/(\d+)', 'delete',
	'/(\w+)/edit/(\d+)', 'edit'
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
		"th": ["Id", "Host", "Share", "Path", "Type", "Organization", "Comments"],
		"td": ["id", "hostname", "sharename", "path", "dbtypename", "orgname", "comments"]
	}
}

class	index:
	def	GET(self):
		return render.index()
		#web.render('index.html')

class	menu:
	def	GET(self):
		return render.menu()

class	acl:
	def	GET(self):
		global userlist, dblist
		# 1. prepare top - users
		userlist = []
		userdict = {}	# id-to-userlist_no mapping
		for i, user in enumerate(mydb.select('user')):
			userlist.append((user.id, user.login, user.comments))
			userdict[user.id] = i
		# 2. prepare left = databases
		dblist = []
		dbdict = {}	# id-to-dblist_no mapping
		dxu = []
		for i, db in enumerate(mydb.select('dblist')):
			dblist.append((db.id, db.path, db.dbtypename, db.orgname, db.comments))
			dbdict[db.id] = i
			dxu.append([False] * len(userlist))
		# 3. and square marix
		for aclitem in mydb.select('acl'):
			if aclitem.visible:
				#print dbdict[aclitem.dbid], userdict[aclitem.userid]
				dxu[dbdict[aclitem.dbid]][userdict[aclitem.userid]] = True
		return render.acl(userlist, dblist, dxu)
	def	POST(self):
		global userlist, dblist
		i = web.input()
		mydb.delete('acl', where="1=1")
		for k in i.keys():
			i, j = k.split('.')
			mydb.insert('acl', userid=userlist[int(j)][0], dbid=dblist[int(i)][0], visible=True)
		raise web.seeother("/acl")

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
		items = mydb.select(dbname)
		if (dbname == 'user'):
			subform = render.useradd()
		elif (dbname in ("dbtype", "org")):
			subform = render.otheradd()
		elif (dbname == 'db'):	# db
			items = mydb.select('dblist')
			dbtypes = mydb.select('dbtype')
			orgs = mydb.select('org')
			subform = render.dbadd(dbtypes, orgs)
		else:
			print "Bad page"
		return render.list(items, dbname, mydict[dbname], subform, msg)
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
				count = mydb.query('SELECT COUNT (*) AS total FROM user WHERE login="%s"' % (i.login))[0].total
				if (count > 0):
					message = "Same login already exists."
				else:
					n = mydb.insert(dbname, login=i.login, password=i.password, comments=i.comments)
					message = "%s %d added ok" % (mydict[dbname]["entry"], n)
		elif (dbname in ("dbtype", "org")):
			i.name = i.name.strip()
			if (i.name == ""):
				message = "Name can't be empty."
			else:
				#print 'SELECT COUNT (*) AS total FROM %s WHERE name="%s"' % (dbname, i.name)
				count = mydb.query('SELECT COUNT (*) AS total FROM %s WHERE name="%s"' % (dbname, i.name))[0].total
				if (count > 0):
					message = "Same name already exists."
				else:
					n = mydb.insert(dbname, name=i.name, comments=i.comments)
					message = "%s %d added ok" % (mydict[dbname]["entry"], n)
		else:	# db
			if not fullpathre.match(i.fullpath):
				message = "Path must be in form: \\\\<host>\\<share>\\<path>"
			else:
				host, share, path = fullpathre.split(i.fullpath.lower())[1:4]
				# cascade insert.
				# 1. Host
				count = mydb.query('SELECT COUNT (*) AS total FROM host WHERE name="%s"' % host)[0].total
				if (count == 0):
					hostid = mydb.insert('host', name=host)
					message = 'Host "%s" added ok.' % host
				else:
					hostid = int(mydb.select('host', where='name="%s"' % host)[0].id)
					count = mydb.query('SELECT COUNT (*) AS total FROM share WHERE hostid="%d" AND name="%s"' % (hostid, share))[0].total
				# 2. Share
				if (count == 0):
					shareid = mydb.insert('share', name=share, hostid=hostid)
					message += '\nShare "%s" added ok.' % share
				else:
					shareid = int(mydb.select('share', where='hostid="%d" AND name="%s"' % (hostid, share))[0].id)
					count = mydb.query('SELECT COUNT (*) AS total FROM db WHERE shareid="%d" AND path="%s"' % (shareid, path))[0].total
				# 3. DB
				if (count == 0):
					id = mydb.insert('db', path=path, shareid=shareid, dbtypeid=int(i.dbtype), orgid=int(i.org), comments=i.comments)
					message += '\nDatabase "%d" added ok.' % id
				else:
					message = "Database already exists"
		raise web.seeother("/%s/list/" % dbname)
class	delete:
	def	GET(self, dbname, id):
		global message, fullpathre
		if (dbname == 'db'):	# cascade up deletion of shares and servers
			id = int(id)
			item = mydb.select(dbname, where="id=%d" % id)[0]
			shareid = int(item.shareid)
			count = mydb.query('SELECT COUNT (*) AS total FROM db WHERE shareid=%d' % shareid)[0].total
			n = mydb.delete(dbname, where="id=%d" % id)	# option
			message = "%d database deleted ok." % n
			if (count == 1):	# check on orphan share
				item = mydb.select('share', where="id=%d" % shareid)[0]
				hostid = int(item.hostid)
				count = mydb.query('SELECT COUNT (*) AS total FROM share WHERE hostid=%d' % hostid)[0].total
				n = mydb.delete('share', where="id=%d" % shareid)	# option
				message += "\n%d share deleted ok." % n
				if (count == 1):	# check on orphan server
					n = mydb.delete('host', where="id=%d" % hostid)
					message += "\n%d host deleted ok." % n
		else:
			n = mydb.delete(dbname, where="id=%d" % int(id))
			message = "%d %s[s] deleted ok" % (n, mydict[dbname]["entry"])
		raise web.seeother("/%s/list/" % dbname)
class	edit:
	def	GET(self, dbname, id):
		global message, mydict
		id = int(id)
		items = mydb.select(dbname)
		item = mydb.select(dbname, where="id = %d" % id)[0]
		if (dbname == 'user'):
			subform = render.useredit(item)
		elif (dbname in ("dbtype", "org")):
			subform = render.otheredit(item)
		elif (dbname == 'db'):	# db
			items = mydb.select('dblist')
			shares = mydb.select('sharelist')
			dbtypes = mydb.select('dbtype')
			orgs = mydb.select('org')
			return render.dbedit(items, id, shares, dbtypes, orgs, message)
		else:
			print "Bad page"
		return render.edit(items, id, dbname, mydict[dbname], subform, message)
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
				count = mydb.query('SELECT COUNT (*) AS total FROM user WHERE id<>%d AND login="%s"' % (id, i.login))[0].total
				if (count > 0):
					message = "Same login already exists."
					nextform = "edit"
				else:
					n = mydb.update(dbname, where="id = %d" % id, login = i.login, password = i.password, comments = i.comments)
					message = "%d %s[s] edited ok" % (n, mydict[dbname]["entry"])
		elif (dbname in ("dbtype", "org")):
			i.name = i.name.strip()
			if (i.name == ""):
				message = "Name can't be empty."
				nextform = "edit"
			else:
				count = mydb.query('SELECT COUNT (*) AS total FROM %s WHERE id<>%d AND name="%s"' % (dbname, id, i.name))[0].total
				if (count > 0):
					message = "Same name already exists."
					nextform = "edit"
				else:
					n = mydb.update(dbname, where="id = %d" % id, name = i.name, comments = i.comments)
					message = "%d %s[s] edited ok" % (n, mydict[dbname]["entry"])
		else:	# db
			i.path = i.path.strip()
			i.path = i.path.strip('/')
			n = mydb.update('db', where="id = %d" % id, shareid = int(i.shareid), dbtypeid = int(i.dbtypeid), orgid = int(i.orgid), path = i.path, comments = i.comments)
			message = "%d %s[s] edited ok" % (n, mydict[dbname]["entry"])
		raise web.seeother("/%s/%s/" % (dbname, nextform))

class	serial:
	def	GET(self):
		return render.baselist(mydb.select('var', where="name='serial'")[0].value)

class	baselist:
	def	GET(self, login, password):
		sn = mydb.select('var', where="name='serial'")[0].value
		count = mydb.query('SELECT COUNT (*) AS total FROM user WHERE login="%s"' % login)[0].total
		if (count == 0):
			return render.baselist(sn, error = "user not found")
		a = mydb.select('user', where="login='%s'" % login)[0]
		if (a.password != password):
			return render.baselist(sn, error = "wrong password")
		else:
			b = mydb.select('baselist', where="userid='%s'" % a.id)
			web.header('Content-Type', 'text/xml')
			return render.baselist(sn, b)

application = web.application(urls, globals()).wsgifunc()

if __name__ == "__main__":
	web.application(urls, globals()).run()

