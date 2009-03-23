#!/bin/env python
# -*- coding: utf-8 -*-
'''
* plugins - as "import ..."
'''

from __future__ import with_statement
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
import config, var, common, soft

web.config.debug = False
var.render = web.template.render('templates/', cache=False)
var.root = ""
if os.path.exists(config.dbfn):
	var.mydb = web.database(dbn='sqlite', db=config.dbfn)
else:
	var.mydb = web.database(dbn='sqlite', db=config.dbfn)
	f = open('sqlite.sql')
	for i in f:
		var.mydb.query(i)

urls = (
	'/', 'index',
	'/soft', 'soft.main',
	'/soft/main/(\w+)/(\d*)', 'soft.main',
	'/soft/vendor/(\w+)/(\d*)', 'soft.vendor',
	'/soft/distrib/(\w+)/(\d*)', 'soft.distrib',
	'/soft/platform/(\w+)/(\d*)', 'soft.platform',
	'/soft/settings', 'soft.settings',
	'/audio', 'audio'
)

class	index:
	def	GET(self):
		return var.render.index()

class	audio:
	def	GET(self):
		f = open(os.path.join(config.filepath, "qsvn.desktop"), "rb")
		web.header("Content-type", "application/octet-stream")
		web.header("Content-Disposition", "inline; filename=\"tratata.desktop\"")
		return f.read()

if __name__ == "__main__":
	web.application(urls, globals()).run()
else:
	var.root = "/thestorage"
	application = web.application(urls, globals()).wsgifunc()
