#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
filter all ctrl tags and show all of their attributes
@author TI_Eugene
"""

import sys
from xml.parsers import expat	# std

def start_element(name, attrs):
	if (name == 'obj'):
		keys = attrs.keys()
		for i in (xrange(len(keys))):	# print each attr
			a = keys[i]
			print name + "\t" + a + "\t\"" + attrs[a] + "\""

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