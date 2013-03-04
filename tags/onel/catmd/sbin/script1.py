#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Get ts & TaskItem attributes.
@author TI_Eugene; 57xx
"""

import sys, locale
from xml.parsers import expat	# std

counter = 2
LOCALE = locale.getdefaultlocale()[1]

def	__UniStr(str):
	'''
	Get UTF-8 string in current locale.
	@author Seryozhin D.V. aka Alon (dm88@bk.ru)
	@author Grishin Alexander aka GrAlex (gralex1974@ua.fm)
	@return Locale encoded string
	'''
	try:
		str = unicode(str,'utf8')	#.encode(LOCALE).decode(LOCALE)
		return str
	except UnicodeError:
		print 'Unicode error!!!'
		return str

def	myfunc(attrs, name, key):
	if attrs.get(key):
		print name + "\t" + __UniStr(attrs[key])

def start_element(name, attrs):
	global counter
	if (counter):
		if (name == 'ts'):
			myfunc(attrs, "TS.Shrt", 'short')
			counter -= 1
		elif (name == 'TaskItem'):
			myfunc(attrs, "TI.id", 'id')
			myfunc(attrs, "TI.syn", 'syn')
			myfunc(attrs, "TI.com", 'com')
			counter -= 1

argv = sys.argv
if (len(argv) != 2):
	print "Usage:", argv[0], "<dir>"
else:
	p = expat.ParserCreate()
	p.returns_unicode = 0
	p.StartElementHandler = start_element
	f = open(argv[1] + "/cfg.xml")
	print "File\t" + argv[1]
	p.ParseFile(f)
	f.close()
