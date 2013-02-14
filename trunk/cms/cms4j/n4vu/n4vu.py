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

Node_form = web.form.Form (
	web.form.Textbox('lastname',	chk_empty, description='Фамилия'),
	web.form.Textbox('firstname',	chk_empty, description='Имя'),
	web.form.Textbox('midname',	description='Отчество'),
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
		return render.node.view(db.nodes.get(int(id)))

class	NodeDel:
	def	GET(self, id):
		db = getdb()
		db.nodes.get(int(id)).delete()
		raise web.seeother('/node/')

# Node parameters
class	NParmEdit:
	def	GET(self):
		return render.nparm.edit()

# Rel
class	RelView:
	def	GET(self, id):
		db = getdb()
		return render.rel.view(db.relationships.get(int(id)))

urls = (
	'/',			'Index',
	'/node/',		'NodeList',
	'/node/add/',		'NodeAdd',
	'/node/([0-9]+)/',	'NodeView',
	'/node/([0-9]+)/del/',	'NodeDel',
	'/nparm/edit/',		'NParmEdit',
	'/rel/([0-9]+)/',	'RelView',
)

# 1. standalone
if __name__ == '__main__':
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()
# 2. apache mod_wsgi
os.chdir(os.path.dirname(__file__))
application = web.application(urls, globals()).wsgifunc()
