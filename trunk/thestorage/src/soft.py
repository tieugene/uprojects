# -*- coding: utf-8 -*-
'''
Software
'''

from __future__ import with_statement
import sys, os, re, hashlib
import var

class	menu:
	def	GET(self):
		return var.render.soft_menu()

class	main:
	def	GET(self, action):
		items = var.mydb.select('programm')
		return var.render.soft_list(var.root, items)
	def	POST(self):
		x = web.input(myfile={})['myfile']
		with open(os.path.join(config.filepath, x.filename), "wb") as f:
			f.write(x.value)
			print hashlib.md5(x.value).hexdigest()
		raise web.seeother('/soft/main/list')

class	vendor:
	def	GET(self, action):
		items = var.mydb.select('vendor')
		return var.render.soft_vendor(var.root, items)

class	distrib:
	def	GET(self, action):
		pass

class	platform:
	def	GET(self, action):
		pass

class	settings:
	def	GET(self, action):
		pass
