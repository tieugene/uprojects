# -*- coding: utf-8 -*-
'''
main module.
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
	@param i:str - input codepage.
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
	if (q):	return a1
	else:		return a2

def	Iso2DateTime(s):
	'''
	converts ISO formated date into datetime.
	'''
	date, time = s.split(" ", 1)
	y, m, d = date.split("-")
	h, mi, s = time.split(":")
	return datetime(int(y), int(m), int(d), int(h), int(mi), int(s))

# trash
##def	PrintData(datalist):
##	rec = 0
##	for d in datalist:
##		rec += 1
##		print rec, "=" * 20
##		for i in xrange(len(fld)):
##			if (d[i]):
##				print "%s:\t%s" % (fld[i], str(d[i]))

##def	TryDefault(v):
##	retvalue = None
##	t = type(v).__name__
##	if (t == "str"):
##		if (v):	retvalue = utility.XCode(v)
##		else:		retvalue = ""
##	elif (t == "int"):
##		if (v):	retvalue = v
##		else:		retvalue = 0
##	return retvalue
