#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
count all REF's & it's UREF's.
@author TI_Eugene
"""

import sys
from xml.parsers import expat

UID = {}	# { uid : [uidobjname, [urefs0, ...]]}

def start_element(name, attrs):
	global UID
	
	keys = attrs.keys()
	for k in keys:
		v = attrs[k]					# key (attr) value
		if (k == 'uid'):
			if v[0] == '_':
				v = long(v[1:])
			tmp = UID.get(v)			# find key
			if (tmp):				# already exists
				if (tmp[0]):			# ... and not empty
					print "Key alreadty exists"
				else:
					UID[v][0] = name	# store uid object
					
			else:					# not exists
				UID[v] = [name, []]		# empty record
		elif (k.startswith('uref')):
			if v[0] == '_':
				v = long(v[1:])
			tmp = UID.get(v)
			if (tmp):				# record exists
				UID[v][1].append(name)		# add new uref object
			else:					# new record
				UID[v] = [None, [name]]

argv = sys.argv
if (len(argv) != 2):
	print "Usage:", argv[0], "<xml_file>"
else:
	p = expat.ParserCreate()
	p.returns_unicode = 0
	p.StartElementHandler = start_element
	f = open(argv[1])
	p.ParseFile(f)
	f.close()
	# out results
	keys = UID.keys()
	keys.sort()
	for k in keys:
		print k, "\t", UID[k][0], "\t", UID[k][1]
		#print name + "\t" + a + "\t\"" + attrs[a] + "\""
