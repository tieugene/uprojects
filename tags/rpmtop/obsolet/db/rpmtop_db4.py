#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
script to dump rpm database files - via db4 interface.
'''
import bsddb, sys, struct, pprint
import load, gvar

def	Out_Results():
	'''
	dump db hash
	'''
	for p in gvar.Pkg:
		print p[0]
		for i in p[1]:
			print "\t%s" % gvar.Svc[i][0]

# ---	main ---
def	main(argv):
	# 0. preparing
	global debugmode, Pkg_Count
	# 1. load data
	load.Load("/var/lib/rpm/")
	# 2. out results
#	Out_Results()

if (__name__ == '__main__'):
	main(sys.argv)
