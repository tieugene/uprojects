#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
filter all ctrl tags and show their typ attribute
@author TI_Eugene
"""

import sys
from xml.parsers import expat	# std

entity = None
attr = None

def start_element(name, attrs):
	global entity, attr
	if (name == entity):
		print "\"" + attrs[attr] + "\""

argv = sys.argv
if (len(argv) != 4):
	print "Usage:", argv[0], "<xml_file> <entity_name> <attr_name>"
else:
	p = expat.ParserCreate()
	p.returns_unicode = 0
	p.StartElementHandler = start_element
	f = open(argv[1])
	entity = argv[2]
	attr = argv[3]
	p.ParseFile(f)
	f.close()
