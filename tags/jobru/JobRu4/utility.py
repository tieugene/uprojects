# -*- coding: utf-8 -*-
'''
utility.py - Utility module.
Misc utility functions.
'''

import locale
from datetime import datetime

KOI8R = 1
CP1251 = 2
UTF8 = 3
CP = ["ascii", "koi8-r", "cp1251", "utf8"]

def     XCode(s, i = None, o = None):
	'''
	Cross-code input text from one codepage to other.
	@param s:str - text to convert.
	@param i:str - input codepage (1:koi, 2:win, 3:utf).
	@param o:str - output codepage; if ommited - locale.
	'''
	retvalue = s
	if (i == None):
		i = CP1251
	if (o == None):
		ocp = locale.getdefaultlocale()[1]
	else:
		ocp = CP[o]
	try:
		return unicode(s, CP[i]).encode(ocp)
	except TypeError:
		print "Can't convert:", s
		return None

def	Ask(q, a1, a2):
	'''
	Selector
	@param q:bool
	@param a1:any
	@param a2:any
	@return a1 (if q == True) or a2 (if q == False)
	'''
	if (q):
		return a1
	else:
		return a2

def	Iso2DateTime(s):
	'''
	Converts ISO formated date into datetime.
	@param s:str - ISO formated date ('YY-MM-DD HH:MM:SS')
	@return datetime value
	'''
	date, time = s.split(" ", 1)
	y, m, d = date.split("-")
	h, mi, s = time.split(":")
	return datetime(int(y), int(m), int(d), int(h), int(mi), int(s))
