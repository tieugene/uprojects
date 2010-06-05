#!/bin/env python
# -*- coding: utf-8 -*-

import	sys, re

key = '19465912879oiuxc ensdfaiuo3i73798kjl'
r = re.compile('{{"Server","(\w+)"},{"DB","(\w+)"},{"UID","(\w+)"},{"PWD","(\w+)"},{"Checksum","(\w+)"}}')

def	main(argv):
	f = open(argv[0])
	s = ''
	if (f):
		for i, c in enumerate(f.read()):
			s += chr(ord(c) ^ ord(key[i % 36]))
	f.close()
	m = r.search(s)
	print m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)

if (__name__ == '__main__'):
	main(sys.argv[1:])
