#!/bin/env python
# -*- coding: utf-8 -*-

'''
Check INN and KPP
'''

import sys, simplejson as json
reload(sys)
sys.setdefaultencoding("utf-8")

def	chkinn(s):
	retvalue = False
	if len(s) == 10:
		retvalue = (((2*int(s[0]) + 4*int(s[1]) + 10*int(s[2]) + 3*int(s[3]) + 5*int(s[4]) + 9*int(s[5]) + 4*int(s[6]) + 6*int(s[7]) + 8*int(s[8])) % 11) % 10) == int(s[9])
	elif len(s) == 12:
		retvalue = \
			(((7*int(s[0]) + 2*int(s[1]) + 4*int(s[2]) + 10*int(s[3]) + 3*int(s[4]) + 5*int(s[5]) + 9*int(s[6]) + 4*int(s[7]) + 6*int(s[8]) + 8*int(s[9])) % 11) % 10) == int(s[10]) and \
			(((3*int(s[0]) + 7*int(s[1]) + 2*int(s[2]) + 4*int(s[3]) + 10*int(s[4]) + 3*int(s[5]) + 5*int(s[6]) + 9*int(s[7]) + 4*int(s[8]) + 6*int(s[9]) + 8*int(s[10])) % 11) % 10) == int(s[11])
	return retvalue

def	chkogrn(s):
	retvalue = False
	if len(s) == 13:
		retvalue = str((long(s[:12]) % 11))[-1] == s[12]
	elif len(s) == 15:
		retvalue = str((long(s[:14]) % 13))[-1] == s[14]
	return retvalue

if (len(sys.argv) != 2):
	print "Usage: %s <infile>" % sys.argv[0]
else:
	data = json.load(open(sys.argv[1], "r"))
	for i in data:
		if (i['model'] == 'sro2.org'):
			a = i['fields']['inn']
			if (chkinn(a) == False):
				print u'%s: ИНН=%s' % (i['fields']['name'], a)
			a = i['fields']['ogrn']
			if (chkogrn(a) == False):
				print u'%s: ОГРН=%s' % (i['fields']['name'], a)
