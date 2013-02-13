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

def	connect():
	global db
	try:
		db = client.GraphDatabase("http://localhost:7474/db/data/")
	except:
		pass

class	Index:
	def	GET(self):
		return render.index()

class	NodeList:
	def	GET(self):
		global db
		if (db == None):
			connect()
			if db == None:
				print "db err"
		q = 'START n=node(*) RETURN n'
		nodes = db.query(q, returns=(client.Node,))
		return render.node_list(nodes)

class	NodeAdd:
	def	GET(self):
		return render.node_add(node_form())

class	NodeView:
	def	GET(self, id):
		global db
		q = 'START n=node(%s) RETURN n' % id
		node = db.query(q, returns=(client.Node,))[0][0]
		#print node.properties
		#for k in node.properties:
		#	print k, node.properties[k]
		return render.node_view(node)

class	NodeEdit:
	def	GET(self):
		return render.node_edit()

class	NodeDel:
	def	GET(self):
		return render.node_del()

urls = (
	'/',		'Index',
	'/node_list/',	'NodeList',
	'/node_add/',	'NodeAdd',
	'/node_view/(.*)',	'NodeView',
	'/node_edit/',	'NodeEdit',
	'/node_del/',	'NodeDel',
)

# 1. standalone
if __name__ == '__main__':
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()
# 2. apache mod_wsgi
os.chdir(os.path.dirname(__file__))
application = web.application(urls, globals()).wsgifunc()
