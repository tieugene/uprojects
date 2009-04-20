#!/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import web
import config, var

web.config.debug = False
var.render = web.template.render('templates/', cache=False)
var.message = ""
var.root = ""
var.menu = var.render.menu(var.root)
if os.path.exists('sro.db'):
	var.db = web.database(dbn='sqlite', db='sro.db')
else:
	var.db = web.database(dbn='sqlite', db='sro.db')
	f = open('sro.sql')
	for i in f:
		var.db.query(i)

urls = (
	'/', 'index',
	'/org/list/', 'org.list',
	'/org/add/', 'org.add',
	'/org/view/(\d+)', 'org.view',
	'/org/edit/(\d+)', 'org.edit',
	'/org/del/(\d+)', 'org.delete',
	'/person/(\w+)/(\d*)', 'person',
	'/meeting/(\w+)/(\d*)', 'meeting',
	'/event/(\w+)/(\d*)', 'event',
	'/profile/(\w+)/(\d*)', 'profile',
	'/user/(\w+)/(\d*)', 'users',
	'/okved/(\w+)/(\d*)', 'okved',
	'/okdp/(\w+)/(\d*)', 'okdp',
	'/okopf/(\w+)/(\d*)', 'okopf',
	'/okpdtr/(\w+)/(\d*)', 'okpdtr',
	'/okso/(\w+)/(\d*)', 'okso'
)

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

class	index:
	def	GET(self):
		return var.render.index(var.menu)

class	org:
	pass

class	person:
	pass

class	meeting:
	pass

class	org:
	pass

class	org:
	pass

class	org:
	pass

class	org:
	pass

class	org:
	pass

if __name__ == "__main__":
	web.application(urls, globals()).run()
else:
	var.root = "/sro"
	var.menu = var.render.menu(var.root)
	application = web.application(urls, globals()).wsgifunc()
