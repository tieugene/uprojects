#!/bin/env python
# -*- coding: utf-8 -*-
'''
N4vu - Neo4j graph viewer
Req: python-webpy
'''

# 3rd parties
try:
	import web
except:
	print "install python-webpy first"
try:
	from neo4jrestclient import client
except:
	print "install python-neo4jrestclient first"
# system
import sys, os, tempfile, pprint, datetime

reload(sys)
sys.setdefaultencoding('utf-8')

db = None
debug = True
cache = False
try:
        from local_settings import *
except ImportError:
        pass

render = web.template.render('templates', base='base', cache=cache)

# validators
chk_empty = web.form.Validator('Обязательное поле', bool)

ptype_list = [
	('1', 'bool'),
	('2', 'int'),
	('3', 'str'),
]

parm_form = web.form.Form (
	web.form.Textbox('name',	chk_empty, description='Name'),
	web.form.Dropdown('type',	description='Type', args=ptype_list, value='3'),
	web.form.Textbox('value',	chk_empty, description='Value'),
)

rdir_list = [
	('1', ' <'),
	('2', ' >'),
]

rel_form = web.form.Form (
	web.form.Dropdown('dir',	description='dir', args=rdir_list, value='1'),
	web.form.Textbox('type',	chk_empty, description='Type'),
	web.form.Textbox('node',	chk_empty, description='Node'),
)

def	getdb():
	global db
	if db == None:
		try:
			db = client.GraphDatabase("http://localhost:7474/db/data/")
		except:
			print "Can't connect db"
			exit()
	return db

class	Index:
	def	GET(self):
		return render.index()

# Nodes
class	NodeList:
	def	GET(self):
		db = getdb()
		return render.node.list(db.query('START n=node(*) RETURN n', returns=(client.Node,)))

class	NodeAdd:
	def	GET(self):
		db = getdb()
		raise web.seeother('/node/%d/' % db.nodes.create().id)

class	NodeView:
	def	GET(self, id):
		db = getdb()
		return render.node.view(db.nodes.get(int(id)), parm_form(), rel_form())

class	NodeDel:
	def	GET(self, id):
		db = getdb()
		db.nodes.get(int(id)).delete()
		raise web.seeother('/node/')

# Node parameters
class	NodeParmAdd:
	def	GET(self, id):
		return render.nparm.edit()

class	NodeParmDel:
	def	GET(self, id, name):
		db = getdb()
		node = db.nodes.get(int(id))
		node.delete(name)
		raise web.seeother('/node/%d/' % node.id)

class	NodeRelDel:
	def	GET(self, id, rel):
		db = getdb()
		db.relationships.get(int(rel)).delete()
		raise web.seeother('/node/%d/' % int(id))

# Rel
class	RelView:
	def	GET(self, id):
		db = getdb()
		return render.rel.view(db.relationships.get(int(id)))

class	RelDel:
	def	GET(self, id):
		db = getdb()
		db.relationships.get(int(id)).delete()
		raise web.seeother('/node/')

urls = (
	'/',				'Index',
	'/node/',			'NodeList',
	'/node/add/',			'NodeAdd',
	'/node/([0-9]+)/',		'NodeView',
	'/node/([0-9]+)/del/',		'NodeDel',
	'/node/([0-9]+)/padd/',		'NodeParmAdd',
	'/node/([0-9]+)/pdel/(.+)',	'NodeParmDel',
	'/node/([0-9]+)/radd/',		'NodeRelAdd',
	'/node/([0-9]+)/rdel/([0-9]+)/',	'NodeRelDel',
	'/rel/([0-9]+)/',		'RelView',
	'/rel/([0-9]+)/del/',		'RelDel',
)

# 1. standalone
if __name__ == '__main__':
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()
# 2. apache mod_wsgi
os.chdir(os.path.dirname(__file__))
application = web.application(urls, globals()).wsgifunc()
