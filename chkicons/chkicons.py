#!/bin/env python
# -*- coding: utf-8 -*-
'''
Tool to check icon theme on FDO compatibility.
Input: rpm -ql *-icon-theme
Output: tab-separated list:
folder	iconname	16	22 ..
======	========	sum	sum
SUMMARY	sum

Algo:
* load fdo.lst into list[(folder, icon)
* load icon theme list
* clean:
-- remove heads
-- remove ext
-- split into size, folder, icon
-- store as dict()...
-- create counters (by size)
* count:
-- for each fdo icon:
--- for each size:
---- find icon
---- print result
---- update counter
'''

import sys, pprint

def	log(s):
	pass
	#print s

def	main(argv):
	FDO = list()
	ICONS = dict()
	COUNTER = dict()
	# 1. load fdo.lst
	for line in open('fdo.lst', 'r').readlines():
		s = line.strip("\n").split("\t")
		FDO.append((s[0], s[1]))
	# 2. load filelist
	for line in open(argv, 'r').readlines():
		if (line.startswith('/usr/share/icons/')):
			s = line.strip("\n").split("/")
			if (len(s) == 8):
				n, e = s[7].rsplit('.', 1)
				if s[5] not in COUNTER:
					COUNTER[s[5]] = 0
				ICONS[(s[5], s[6], n)] = True	# size, folder, icon
	# 3. count
	SIZES = COUNTER.keys()
	SIZES.sort()
	print "Folder\tIcon\t%s" % "\t".join(SIZES)
	print "======\t====%s" % ("\t===" * len(SIZES))
	for f, i in FDO:
		line = "%s\t%s" % (f, i)
		for s in SIZES:
			if (s, f, i) in ICONS:
				line += "\t+"
				COUNTER[s] += 1
			else:
				line += "\t-"
		print line
	# X. the end
	print "======\t====%s" % ("\t===" * len(SIZES))
	s = "Summ:\t%s" % len(FDO)
	for i in SIZES:
		s += "\t%d" % COUNTER[i]
	print s

if (__name__ == '__main__'):
	argv = sys.argv
	if (len(argv) != 2):
		print "Usage: %s <filelist>" % sys.argv[0]
	else:
		main(sys.argv[1])
