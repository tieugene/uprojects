#!/bin/env python
# -*- coding: utf-8 -*-
'''
* plugins - as "import ..."
'''

from __future__ import with_statement
import sys, os, re
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
import config

web.config.debug = False
render = web.template.render('templates/', cache=False)
root = ""
if os.path.exists(config.dbfn):
	mydb = web.database(dbn='sqlite', db=config.dbfn)
else:
	mydb = web.database(dbn='sqlite', db=config.dbfn)
	f = open('sqlite.sql')
	for i in f:
		mydb.query(i)

urls = (
	'/', 'index',
	'/menu', 'menu',
	'/programm', 'programm'
)

class	index:
	def	GET(self):
		return render.index()

class	menu:
	def	GET(self):
		return render.menu()

class	programm:
	def	GET(self):
		items = mydb.select('programm')
		return render.programm(root, items)
	def	POST(self):
		x = web.input(myfile={})['myfile']
		with open(config.filepath + "/" + x.filename, "wb") as f:
			f.write(x.value)
		raise web.seeother('/programm')

if __name__ == "__main__":
	web.application(urls, globals()).run()
else:
	root = "/run1s"
	application = web.application(urls, globals()).wsgifunc()
