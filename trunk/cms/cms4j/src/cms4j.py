#!/bin/env python
# -*- coding: utf-8 -*-
'''
Req: python-webpy
Run: 
try: web2py bottle flask pyramid cherripy
'''

# 3rd parties
import web
# system
import sys, os, tempfile, pprint, datetime

reload(sys)
sys.setdefaultencoding('utf-8')

debug = True
cache = False
try:
        from local_settings import *
except ImportError:
        pass
render = web.template.render('templates', base='base', cache=cache)

class	index:
	def	GET(self):
		return render.index()

class	core:
	def	GET(self):
		return render.core()

urls = (
	'/', 'index',
	'/core/', 'core',
)

# 1. standalone
if __name__ == '__main__':
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()
# 2. apache mod_wsgi
os.chdir(os.path.dirname(__file__))
application = web.application(urls, globals()).wsgifunc()
